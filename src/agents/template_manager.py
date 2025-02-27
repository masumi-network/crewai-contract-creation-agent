from crewai import Agent
from ..tools.contract_tools import ContractTools

class TemplateManagerAgent:
    def __init__(self):
        self.tools = ContractTools()
        
    def create_agent(self):
        return Agent(
            role='Template Manager',
            goal='Manage and customize contract templates based on requirements',
            backstory="""You are a contract template specialist with expertise in creating 
            and managing various types of legal document templates. You understand different 
            business needs and can adapt templates accordingly.""",
            tools=self.tools.get_tools(),
            verbose=True,
            allow_delegation=False
        ) 