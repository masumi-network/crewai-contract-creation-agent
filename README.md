# crewai-contract-creationa-gent

I'll create a comprehensive README for the project.

```markdown:README.md
# Contract Creation Agent with CrewAI

This project implements an intelligent contract creation system using CrewAI, which automates the process of generating and reviewing legal documents through a multi-agent approach.

## 🌟 Features

- **Automated Contract Generation**: Creates contracts from templates with custom variables
- **Legal Review**: Automated legal compliance checking
- **Multiple Contract Types**: Supports NDA, Freelance, and Employment contracts
- **API Interface**: FastAPI-based REST API for easy integration
- **Database Storage**: PostgreSQL integration for contract management
- **Docker Support**: Easy deployment with Docker and Docker Compose

## 🏗️ Architecture

The system uses multiple specialized agents working together:

1. **Contract Writer Agent**: Creates initial contract drafts using templates
2. **Legal Reviewer Agent**: Reviews contracts for legal compliance
3. **Template Manager Agent**: Manages and customizes contract templates

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/contract-creation-agent.git
cd contract-creation-agent
```

2. Create and configure the `.env` file:
```bash
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql://user:password@localhost:5432/contracts_db
```

3. Build and run with Docker Compose:
```bash
docker-compose up --build
```

### Running Locally (Without Docker)

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn src.api.main:app --reload
```

## 📝 API Usage

### Create a Contract

```bash
curl -X POST http://localhost:8000/create-contract \
-H "Content-Type: application/json" \
-d '{
    "template_type": "nda",
    "variables": {
        "date": "2024-02-14",
        "company_name": "Tech Corp",
        "recipient_name": "John Doe",
        "confidential_info_definition": "All proprietary information",
        "obligations": "Maintain strict confidentiality",
        "duration": "2 years",
        "jurisdiction": "California, USA"
    }
}'
```

## 📁 Project Structure

```
contract-creation-agent/
├── src/
│   ├── agents/           # CrewAI agents
│   ├── tools/            # Agent tools
│   ├── api/              # FastAPI application
│   ├── config/           # Configuration
│   └── templates/        # Contract templates
├── .env                  # Environment variables
├── docker-compose.yml    # Docker composition
├── Dockerfile           # Docker build file
└── requirements.txt     # Python dependencies
```

## 🛠️ Available Templates

1. **NDA (Non-Disclosure Agreement)**
   - Basic confidentiality agreement
   - Customizable terms and conditions

2. **Freelance Contract**
   - Project-based agreement
   - Payment terms
   - Deliverables specification

3. **Employment Contract**
   - Full-time employment agreement
   - Benefits and compensation
   - Role responsibilities

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: PostgreSQL connection string

### Database

The system uses PostgreSQL for storing:
- Generated contracts
- Contract templates
- Contract metadata

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Future Enhancements

- Digital signature integration (DocuSign/Adobe Sign)
- Blockchain-based contract verification
- Advanced template customization
- Multi-language support
- PDF/DOCX export functionality
- Payment integration (Stripe/PayPal)

## ⚠️ Disclaimer

This is a tool to assist in contract creation but should not replace legal counsel. Always have important legal documents reviewed by qualified legal professionals.

## 🤝 Support

For support, please open an issue in the GitHub repository or contact the maintainers.
```

This README provides a comprehensive overview of the project, including setup instructions, usage examples, and future development plans. It's written in English and follows common documentation best practices. Would you like me to expand on any particular section?



Example of Contract Request:

{
    "template_type": "nda",
    "variables": {
        "date": "2024-02-27",
        "company_name": "Tech Innovations GmbH",
        "recipient_name": "Max Mustermann",
        "confidential_info_definition": "All intellectual property, trade secrets, customer data, and proprietary technologies",
        "obligations": "Keep all information strictly confidential, use only for business purposes, and return all materials upon request",
        "duration": "3 years",
        "jurisdiction": "Germany"
    },
    "customizations": {
        "additional_clauses": "This agreement is also binding for all subsidiaries and affiliated companies",
        "special_terms": "Any breach of this agreement will result in immediate legal action and potential damages of up to €100,000"
    }
}


Alternative test cases:
Freelance Contract:
{
    "template_type": "freelance",
    "variables": {
        "date": "2024-02-27",
        "client_name": "Digital Solutions GmbH",
        "freelancer_name": "Anna Schmidt",
        "project_description": "Development of a web-based CRM system",
        "payment_terms": "€80 per hour, invoiced monthly",
        "delivery_timeline": "3 months",
        "jurisdiction": "Berlin, Germany"
    },
    "customizations": {
        "intellectual_property": "All developed code and assets belong to the client",
        "termination_clause": "30 days written notice required for early termination"
    }
}


Employment Contract:
{
    "template_type": "employment",
    "variables": {
        "date": "2024-02-27",
        "employer_name": "Software Solutions AG",
        "employee_name": "Lisa Weber",
        "position": "Senior Software Engineer",
        "start_date": "2024-03-15",
        "salary": "€75,000 per year",
        "location": "Munich, Germany"
    },
    "customizations": {
        "benefits": "30 days vacation, health insurance, pension plan",
        "working_hours": "40 hours per week with flexible scheduling",
        "probation_period": "6 months"
    }
}

