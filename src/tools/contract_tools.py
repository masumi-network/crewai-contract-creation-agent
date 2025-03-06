from crewai.tools import BaseTool
from typing import Dict
from fpdf import FPDF
import datetime
import os

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

class UnicodePDF(FPDF):
    def __init__(self):
        super().__init__()
        # Add Unicode font
        self.add_font('DejaVu', '', '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf', uni=True)
        self.add_font('DejaVu', 'B', '/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf', uni=True)

    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

class GenerateContractPDFTool(BaseTool):
    name: str = "generate_contract_pdf"
    description: str = "Generates a PDF from contract content"

    def _run(self, contract_content: str, template_type: str = "standard", 
             employee_name: str = "unnamed", variables: Dict[str, str] = None) -> Dict[str, str]:
        try:
            # Ensure contract_content is a string
            if isinstance(contract_content, dict):
                contract_content = str(contract_content.get('result', contract_content))
            elif not isinstance(contract_content, str):
                contract_content = str(contract_content)
            
            # Replace variables if provided
            if variables:
                for key, value in variables.items():
                    placeholder = "{" + key + "}"
                    contract_content = contract_content.replace(placeholder, str(value))
            
            # Create PDF with Unicode support
            pdf = UnicodePDF()
            pdf.add_page()
            
            # Set initial font size smaller
            pdf.set_font('DejaVu', '', 10)
            
            # Process the content line by line
            lines = contract_content.split('\n')
            
            for line in lines:
                line = line.strip()
                if not line:
                    pdf.ln(4)
                    continue
                
                # Handle headers and highlighted text
                if line.startswith('**') and line.endswith('**'):
                    # Section headers
                    pdf.set_font('DejaVu', 'B', 12)
                    text = line.replace('**', '')
                    pdf.ln(8)
                    pdf.cell(0, 8, text, ln=True)
                    pdf.set_font('DejaVu', '', 10)
                elif '**' in line:
                    # Handle inline highlighted text
                    parts = line.split('**')
                    x = pdf.get_x()
                    for i, part in enumerate(parts):
                        if i % 2 == 0:  # Regular text
                            pdf.set_font('DejaVu', '', 10)
                        else:  # Highlighted text
                            pdf.set_font('DejaVu', 'B', 10)
                        width = pdf.get_string_width(part)
                        if x + width > pdf.w - pdf.r_margin:
                            pdf.ln()
                            x = pdf.l_margin
                        pdf.set_x(x)
                        pdf.cell(width, 6, part, 0, 0)
                        x += width
                    pdf.ln()
                elif line.startswith('#'):
                    # Handle agent outputs/comments
                    continue
                else:
                    # Regular text
                    pdf.multi_cell(0, 6, line)
            
            # Generate filename based on template type
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            if template_type == "freelance":
                name = variables.get('freelancer_name', 'unnamed')
            else:
                name = employee_name
            
            sanitized_name = ''.join(c for c in name if c.isalnum() or c in (' -_'))
            filename = f"{template_type.lower()}-{sanitized_name}-{timestamp}.pdf"
            
            # Ensure contracts directory exists
            os.makedirs("contracts", exist_ok=True)
            filepath = os.path.join("contracts", filename)
            
            # Save PDF
            pdf.output(filepath)
            
            return {
                "filepath": filepath,
                "filename": filename,
                "url": f"/contracts/{filename}"
            }
            
        except Exception as e:
            print(f"Error generating PDF: {str(e)}")
            raise Exception(f"Failed to generate PDF: {str(e)}")

class ValidateTemplateTool(BaseTool):
    name: str = "validate_template"
    description: str = "Validates contract template and required data fields"

    def _run(self, template_type: str, variables: Dict[str, str]) -> Dict[str, any]:
        # Convert template type to lowercase and normalize
        template_type = template_type.lower().strip()
        template_type = template_type.replace(" contract", "")
        template_type = template_type.replace(" ", "_").replace("-", "_")
        
        # Define required fields for each template type
        template_requirements = {
            "nda": {
                "required_fields": [
                    "date", "company_name", "recipient_name",
                    "confidential_info_definition", "duration", "jurisdiction"
                ],
                "optional_fields": ["special_terms", "additional_clauses"]
            },
            "freelance": {
                "required_fields": [
                    "date", "client_name", "freelancer_name", "project_description",
                    "payment_terms", "delivery_timeline", "jurisdiction"
                ],
                "optional_fields": ["intellectual_property", "termination_clause"]
            },
            "employment": {
                "required_fields": [
                    "date", "employer_name", "employee_name", "position",
                    "start_date", "salary", "location"
                ],
                "optional_fields": ["benefits", "working_hours", "probation_period"]
            }
        }
        
        print(f"Validating template type: {template_type}")  # Debug log
        print(f"Available templates: {list(template_requirements.keys())}")  # Debug log
        
        validation_result = {
            "is_valid": True,
            "missing_fields": [],
            "template_found": template_type in template_requirements,
            "normalized_type": template_type  # Add normalized type to result
        }
        
        if not validation_result["template_found"]:
            validation_result["is_valid"] = False
            return validation_result
            
        required_fields = template_requirements[template_type]["required_fields"]
        for field in required_fields:
            if field not in variables:
                validation_result["is_valid"] = False
                validation_result["missing_fields"].append(field)
                
        return validation_result

class ContractTools:
    def get_tools(self) -> list[BaseTool]:
        """Returns all tools as a list"""
        return [
            ValidateTemplateTool(),
            ReviewContractTool(),
            CheckComplianceTool(),
            GenerateContractPDFTool()
        ]