from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict
from crewai import Crew, Task
from src.agents.contract_writer import ContractWriterAgent
from src.agents.legal_reviewer import LegalReviewerAgent
from src.tools.contract_tools import ContractTools
from src.agents.template_manager import TemplateManagerAgent
from src.templates.base_templates import ContractTemplate
import os
import json
import re
import datetime

app = FastAPI()

# Mount the contracts directory to serve files
app.mount("/contracts", StaticFiles(directory="contracts"), name="contracts")

class ContractRequest(BaseModel):
    template_type: str
    variables: Dict[str, str]
    customizations: Dict[str, str] = {}

@app.post("/create-contract")
async def create_contract(request: ContractRequest):
    try:
        # Initialize agents
        template_manager = TemplateManagerAgent()
        contract_writer = ContractWriterAgent()
        legal_reviewer = LegalReviewerAgent()
        
        # Create agents
        template_agent = template_manager.create_agent()
        writer_agent = contract_writer.create_agent()
        reviewer_agent = legal_reviewer.create_agent()
        
        # Ensure required variables are present
        required_variables = {
            "employment": ["date", "employer_name", "employee_name", "position", 
                         "salary", "start_date", "location", "jurisdiction", 
                         "employee_address", "duties", "benefits", 
                         "working_hours", "probation_period"],
            "freelance": ["date", "client_name", "client_address", "client_title",
                         "freelancer_name", "freelancer_address", "project_description",
                         "payment_terms", "delivery_timeline", "jurisdiction"],
            "nda": ["date", "company_name", "company_address", "company_title",
                   "recipient_name", "recipient_address", "confidential_info_definition",
                   "permitted_use", "duration", "jurisdiction"]
        }
        
        template_type = request.template_type.lower()
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
        
        # Generate initial contract structure
        try:
            initial_contract = template_manager.prepare_contract_structure(
                template_type,
                request.variables,
                request.customizations
            )
        except Exception as e:
            print(f"Error preparing contract structure: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid template or variables: {str(e)}")
        
        # Create crew with sequential tasks
        crew = Crew(
            agents=[template_agent, writer_agent, reviewer_agent],
            tasks=[
                Task(
                    description=f"Validate the following contract structure and ensure all required fields are present:\n\n{initial_contract}",
                    agent=template_agent,
                    expected_output="Validation results and any required modifications to the contract structure"
                ),
                Task(
                    description=f"Expand and enhance the following contract with detailed content:\n\n{initial_contract}",
                    agent=writer_agent,
                    expected_output="Enhanced contract content with detailed sections and professional formatting"
                ),
                Task(
                    description="Review the final contract for legal compliance and completeness.",
                    agent=reviewer_agent,
                    expected_output="Legal review results and final contract content with compliance confirmation"
                )
            ]
        )
        
        # Execute the crew
        result = crew.kickoff()
        
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