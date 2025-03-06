from crewai import Agent
from ..tools.contract_tools import ContractTools

class ContractWriterAgent:
    def __init__(self):
        self.tools = ContractTools()
        
    def create_agent(self):
        return Agent(
            role='Contract Writer',
            goal='Expand and enhance contract content with detailed explanations',
            backstory="""You are an expert contract writer who takes the initial contract structure and:
            1. Expands each section with comprehensive details
            2. Adds specific examples and scenarios
            3. Ensures legal compliance and clarity
            4. Maintains professional formatting
            
            For each section, you must:
            - Add 3-4 detailed paragraphs of explanation
            - Include relevant examples
            - Add legal context and implications
            - Ensure all terms are clearly defined""",
            tools=[
                self.tools.get_tools()[1],  # review_contract
                self.tools.get_tools()[2],  # check_compliance
            ],
            verbose=True,
            allow_delegation=False
        ) 