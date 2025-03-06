from crewai import Agent
from ..tools.contract_tools import ContractTools

class LegalReviewerAgent:
    def __init__(self):
        self.tools = ContractTools()
        
    def create_agent(self):
        return Agent(
            role='Legal Reviewer',
            goal='Review contracts for legal compliance, consistency, and potential risks with focus on jurisdiction-specific requirements',
            backstory="""You are an experienced international legal professional specialized in contract law 
            across multiple jurisdictions. Your expertise includes:
            - Deep knowledge of contract law in various countries
            - Understanding of jurisdiction-specific requirements
            - Experience with international business contracts
            - Expertise in data protection laws (GDPR, CCPA, etc.)
            - Knowledge of employment law across different regions
            
            You meticulously review contracts to ensure they comply with local laws and regulations,
            identify potential risks, and suggest necessary modifications based on the specific jurisdiction.""",
            tools=[
                self.tools.get_tools()[0],  # validate_template
                self.tools.get_tools()[1],  # review_contract
                self.tools.get_tools()[2],  # check_compliance
            ],
            verbose=True,
            allow_delegation=False
        ) 