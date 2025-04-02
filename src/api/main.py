from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict
from src.tools.contract_tools import ContractTools
from src.templates.base_templates import ContractTemplate
from src.api.crew_manager import ContractCrewManager
import os
import datetime

app = FastAPI()

# Mount the contracts directory to serve files
app.mount("/contracts", StaticFiles(directory="contracts"), name="contracts")

class ContractRequest(BaseModel):
    template_type: str
    variables: Dict[str, str]
    customizations: Dict[str, str] = {}
    language: str = "English"  # Default to English if not specified

@app.post("/create-contract")
async def create_contract(request: ContractRequest):
    try:
        # Initialize crew manager
        crew_manager = ContractCrewManager()
        
        template_type = request.template_type.lower()
        required_variables = crew_manager.get_required_variables()
        
        if template_type not in required_variables:
            raise HTTPException(status_code=400, detail=f"Unsupported template type: {template_type}")
            
        # Load template to get required fields
        template = ContractTemplate(template_type)
        required_fields = template.required_fields
        
        # Check for missing required fields
        missing_vars = [field for field in required_fields 
                      if field not in request.variables]
        if missing_vars:
            raise HTTPException(status_code=400, 
                              detail=f"Missing required variables: {', '.join(missing_vars)}")
        
        # Generate initial contract structure using crew manager
        try:
            initial_contract = crew_manager.prepare_contract_structure(
                template_type,
                request.variables,
                request.customizations
            )
        except Exception as e:
            print(f"Error preparing contract structure: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid template or variables: {str(e)}")
        
        # Execute the crew with language preference
        result = crew_manager.create_and_execute_crew(
            initial_contract,
            language=request.language
        )
        
        # Generate PDF using the final contract content
        tools = ContractTools()
        pdf_tool = tools.get_tools()[3]  # GenerateContractPDFTool
        
        # Get the appropriate name for the PDF based on template type
        recipient_name = ""
        if template_type == "freelance":
            recipient_name = request.variables.get('freelancer_name', 'unnamed')
        elif template_type == "employment":
            recipient_name = request.variables.get('employee_name', 'unnamed')
        elif template_type == "nda":
            recipient_name = request.variables.get('recipient_name', 'unnamed')
        
        try:
            pdf_info = pdf_tool._run(
                contract_content=result,
                template_type=template_type,
                employee_name=recipient_name,
                variables=request.variables
            )
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate PDF")
            
        return JSONResponse({
            "status": "success",
            "contract": {
                "type": template_type,
                "recipient": recipient_name,
                "file_url": pdf_info["url"],
                "generated_at": datetime.datetime.now().isoformat()
            }
        })
            
    except Exception as e:
        print(f"Error in create_contract: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/contracts/{filename}")
async def get_contract(filename: str):
    filepath = os.path.join("contracts", filename)
    if os.path.exists(filepath):
        return FileResponse(filepath, media_type="application/pdf")
    raise HTTPException(status_code=404, detail="Contract not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 