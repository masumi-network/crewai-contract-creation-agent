from crewai import Crew, Task
from src.agents.contract_writer import ContractWriterAgent
from src.agents.legal_reviewer import LegalReviewerAgent
from src.agents.template_manager import TemplateManagerAgent
from typing import Dict

class ContractCrewManager:
    def __init__(self):
        # Initialize agents
        self.template_manager = TemplateManagerAgent()
        contract_writer = ContractWriterAgent()
        legal_reviewer = LegalReviewerAgent()
        
        # Create agents
        self.template_agent = self.template_manager.create_agent()
        self.writer_agent = contract_writer.create_agent()
        self.reviewer_agent = legal_reviewer.create_agent()
        
    def prepare_contract_structure(self, template_type: str, variables: Dict[str, str], 
                                 customizations: Dict[str, str]) -> str:
        """Prepares the initial contract structure using the template manager"""
        return self.template_manager.prepare_contract_structure(
            template_type,
            variables,
            customizations
        )
        
    def create_and_execute_crew(self, initial_contract: str, language: str = "English") -> str:
        """Creates and executes a crew for contract generation and review"""
        # Add language instruction to each task
        language_instruction = f"\nGenerate the contract in {language}. Ensure all legal terms and conditions are accurately translated and maintain their legal meaning."
        
        crew = Crew(
            agents=[self.template_agent, self.writer_agent, self.reviewer_agent],
            tasks=[
                Task(
                    description=f"Validate the following contract structure and ensure all required fields are present. {language_instruction}\n\n{initial_contract}",
                    agent=self.template_agent,
                    expected_output=f"Validation results and any required modifications to the contract structure in {language}"
                ),
                Task(
                    description=f"Expand and enhance the following contract with detailed content. {language_instruction}\n\n{initial_contract}",
                    agent=self.writer_agent,
                    expected_output=f"Enhanced contract content with detailed sections and professional formatting in {language}"
                ),
                Task(
                    description=f"Review the final contract for legal compliance and completeness. Ensure all legal terms are correctly translated and maintain their legal meaning in {language}.",
                    agent=self.reviewer_agent,
                    expected_output=f"Legal review results and final contract content with compliance confirmation in {language}"
                )
            ]
        )
        
        return crew.kickoff()
        
    @staticmethod
    def get_required_variables() -> Dict[str, list]:
        """Returns the required variables for each contract type"""
        return {
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