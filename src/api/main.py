from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from crewai import Crew, Task
from src.agents.contract_writer import ContractWriterAgent
from src.agents.legal_reviewer import LegalReviewerAgent
from src.agents.template_manager import TemplateManagerAgent

app = FastAPI()

class ContractRequest(BaseModel):
    template_type: str
    variables: Dict[str, str]
    customizations: Dict[str, str] = {}

@app.post("/create-contract")
async def create_contract(request: ContractRequest):
    try:
        # Initialize agents
        template_manager = TemplateManagerAgent().create_agent()
        contract_writer = ContractWriterAgent().create_agent()
        legal_reviewer = LegalReviewerAgent().create_agent()
        
        # Create crew
        crew = Crew(
            agents=[template_manager, contract_writer, legal_reviewer],
            tasks=[
                Task(
                    description=f"Get and customize the {request.template_type} template with: {request.customizations}",
                    agent=template_manager,
                    expected_output="A customized contract template ready for variable insertion"
                ),
                Task(
                    description=f"Create a {request.template_type} contract with the following variables: {request.variables}",
                    agent=contract_writer,
                    expected_output="A complete contract with all variables inserted and properly formatted"
                ),
                Task(
                    description="Review the contract for legal compliance and potential issues",
                    agent=legal_reviewer,
                    expected_output="A detailed review report including compliance status, risks, and suggestions"
                )
            ]
        )
        
        # Execute the crew
        result = crew.kickoff()
        
        return {"contract": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 