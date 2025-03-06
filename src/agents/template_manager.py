from crewai import Agent
from ..tools.contract_tools import ContractTools
from ..templates.base_templates import ContractTemplate

class TemplateManagerAgent:
    def __init__(self):
        self.tools = ContractTools()
        
    def create_agent(self):
        return Agent(
            role='Template Manager',
            goal='Manage and validate contract templates and their required fields',
            backstory="""You are an expert in contract template management, responsible for:
            - Validating contract templates against requirements
            - Ensuring all required fields are present
            - Preparing initial contract structures
            - Managing template versioning and compliance""",
            tools=[self.tools.get_tools()[0]],  # ValidateTemplateTool
            verbose=True,
            allow_delegation=False
        )
        
    def prepare_contract_structure(self, template_type: str, variables: dict, customizations: dict = None) -> str:
        """
        Prepares the initial contract structure based on template type and variables.
        """
        try:
            # Load template
            template = ContractTemplate(template_type)
            
            # Build contract content from sections
            contract_content = ""
            for section_name, section_content in template.sections.items():
                # Apply variables to section
                section_text = section_content
                for key, value in variables.items():
                    placeholder = "{" + key + "}"
                    if placeholder in section_text:
                        section_text = section_text.replace(placeholder, str(value))
                
                # Apply any customizations
                if customizations and section_name in customizations:
                    section_text = customizations[section_name]
                
                contract_content += section_text + "\n\n"
            
            return contract_content.strip()
            
        except Exception as e:
            print(f"Error preparing contract structure: {str(e)}")
            raise ValueError(f"Failed to prepare contract: {str(e)}") 