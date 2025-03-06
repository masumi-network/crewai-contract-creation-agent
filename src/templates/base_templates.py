from typing import Dict, List
import json
import os

class ContractTemplate:
    def __init__(self, template_type: str):
        self.template_type = template_type
        self.sections: Dict[str, str] = {}
        self.required_fields: List[str] = []
        self.optional_fields: List[str] = []
        self._load_template()
    
    def _load_template(self):
        """Load template from JSON file"""
        template_path = os.path.join(
            os.path.dirname(__file__), 
            'json', 
            f'{self.template_type.lower()}.json'
        )
        
        if not os.path.exists(template_path):
            raise ValueError(f"Template {self.template_type} not found")
            
        with open(template_path, 'r') as f:
            data = json.load(f)
            self.sections = data['sections']
            self.required_fields = data['required_fields']
            self.optional_fields = data.get('optional_fields', [])

    def get_section(self, section_name: str) -> str:
        """Get template section with placeholders"""
        return self.sections.get(section_name, "") 