from crewai import Agent
from ..tools.contract_tools import ContractTools

class ContractWriterAgent:
    def __init__(self):
        self.tools = ContractTools()
        
    def create_agent(self):
        return Agent(
            role='Contract Writer',
            goal='Create well-structured and legally sound contracts based on templates and requirements',
            backstory="""You are an experienced contract writer with extensive knowledge in creating 
            various types of legal documents. You understand legal terminology and best practices in 
            contract creation.""",
            tools=self.tools.get_tools(),
            verbose=True,
            allow_delegation=False
        ) 