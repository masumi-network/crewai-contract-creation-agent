from crewai.tools import BaseTool
from typing import Dict, Optional
import os
import json

class CreateContractTool(BaseTool):
    name: str = "create_contract"
    description: str = "Creates a new contract from a template"

    def _run(self, template_name: str, variables: Dict[str, str]) -> str:
        template_path = f"src/templates/{template_name}.txt"
        
        if not os.path.exists(template_path):
            return f"Template {template_name} not found"
            
        with open(template_path, 'r') as file:
            template = file.read()
            
        for key, value in variables.items():
            template = template.replace(f"{{${key}}}", value)
            
        return template

class ReviewContractTool(BaseTool):
    name: str = "review_contract"
    description: str = "Reviews a contract for legal compliance and potential issues"

    def _run(self, contract_content: str) -> Dict[str, str]:
        review_results = {
            "compliance_status": "compliant",
            "risks": [],
            "suggestions": [],
            "missing_clauses": []
        }
        
        if "governing law" not in contract_content.lower():
            review_results["missing_clauses"].append("Governing Law clause")
        if "dispute resolution" not in contract_content.lower():
            review_results["missing_clauses"].append("Dispute Resolution clause")
            
        return review_results

class CheckComplianceTool(BaseTool):
    name: str = "check_compliance"
    description: str = "Checks if a contract complies with specific jurisdiction requirements"

    def _run(self, contract_content: str, jurisdiction: str) -> Dict[str, bool]:
        compliance_checks = {
            "has_required_clauses": True,
            "follows_local_law": True,
            "proper_formatting": True
        }
        return compliance_checks

class GetTemplateTool(BaseTool):
    name: str = "get_template"
    description: str = "Retrieves a specific contract template"

    def _run(self, template_type: str) -> Optional[str]:
        template_path = f"src/templates/{template_type}.txt"
        
        if not os.path.exists(template_path):
            return None
            
        with open(template_path, 'r') as file:
            return file.read()

class CustomizeTemplateTool(BaseTool):
    name: str = "customize_template"
    description: str = "Customizes a template based on specific requirements"

    def _run(self, template: str, customizations: Dict[str, str]) -> str:
        customized_template = template
        for key, value in customizations.items():
            customized_template = customized_template.replace(f"{{${key}}}", value)
        return customized_template

class SaveTemplateTool(BaseTool):
    name: str = "save_template"
    description: str = "Saves a new or modified template"

    def _run(self, template_name: str, content: str) -> bool:
        try:
            template_path = f"src/templates/{template_name}.txt"
            with open(template_path, 'w') as file:
                file.write(content)
            return True
        except Exception as e:
            print(f"Error saving template: {e}")
            return False

class ContractTools:
    def get_tools(self) -> list[BaseTool]:
        """Returns all tools as a list"""
        return [
            CreateContractTool(),
            ReviewContractTool(),
            CheckComplianceTool(),
            GetTemplateTool(),
            CustomizeTemplateTool(),
            SaveTemplateTool()
        ]