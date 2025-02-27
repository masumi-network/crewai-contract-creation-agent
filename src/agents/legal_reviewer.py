from crewai import Agent
from ..tools.contract_tools import ContractTools

class LegalReviewerAgent:
    def __init__(self):
        self.tools = ContractTools()
        
    def create_agent(self):
        return Agent(
            role='Legal Reviewer',
            goal='Review contracts for legal compliance, consistency, and potential risks',
            backstory="""You are an experienced legal professional specialized in contract law. 
            Your role is to review contracts for legal compliance, identify potential risks, 
            and ensure all clauses are properly structured and enforceable.""",
            tools=self.tools.get_tools(),
            verbose=True,
            allow_delegation=False
        ) 