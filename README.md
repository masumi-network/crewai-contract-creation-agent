# crewai-contract-creation-agent

# Contract Creation Agent with CrewAI

This project implements an intelligent contract creation system using CrewAI, which automates the process of generating and reviewing legal documents through a multi-agent approach.

## 🌟 Features

- **Automated Contract Generation**: Creates contracts from templates with custom variables
- **Legal Review**: Automated legal compliance checking
- **Multiple Contract Types**: Supports NDA, Freelance, and Employment contracts
- **API Interface**: FastAPI-based REST API for easy integration
- **Database Storage**: PostgreSQL integration for contract management
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **PDF Generation**: Automatic PDF generation with Unicode support
- **Template Validation**: Built-in template and field validation

## 🏗️ Architecture

The system uses multiple specialized agents working together:

1. **Contract Writer Agent**: Creates initial contract drafts using templates and expands content with detailed explanations
2. **Legal Reviewer Agent**: Reviews contracts for legal compliance across multiple jurisdictions
3. **Template Manager Agent**: Manages and customizes contract templates with validation

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/crewai-contract-creation-agent.git
cd crewai-contract-creation-agent
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
        "date": "2024-02-27",
        "company_name": "Tech Innovations GmbH",
        "company_address": "123 Tech Street",
        "company_title": "Technology Company",
        "recipient_name": "Max Mustermann",
        "recipient_address": "456 Innovation Ave",
        "confidential_info_definition": "All intellectual property, trade secrets, customer data, and proprietary technologies",
        "permitted_use": "Business collaboration purposes only",
        "duration": "3 years",
        "jurisdiction": "Germany"
    },
    "customizations": {
        "additional_clauses": "This agreement is also binding for all subsidiaries and affiliated companies",
        "special_terms": "Any breach of this agreement will result in immediate legal action and potential damages of up to €100,000"
    }
}'
```

## 📁 Project Structure

```
crewai-contract-creation-agent/
├── src/
│   ├── agents/           # CrewAI agents (Contract Writer, Legal Reviewer, Template Manager)
│   ├── tools/            # Agent tools (Contract validation, review, PDF generation)
│   ├── api/              # FastAPI application
│   ├── templates/        # Contract templates
│   └── config/          # Configuration files
├── contracts/           # Generated contract PDFs
├── .env                 # Environment variables
├── docker-compose.yml   # Docker composition
├── Dockerfile          # Docker build file
└── requirements.txt    # Python dependencies
```

## 🛠️ Available Templates

1. **NDA (Non-Disclosure Agreement)**
   - Confidentiality terms and conditions
   - Information usage restrictions
   - Duration and jurisdiction specifications
   - Customizable penalties and special terms

2. **Freelance Contract**
   - Project scope and deliverables
   - Payment terms and conditions
   - Intellectual property rights
   - Termination clauses
   - Jurisdiction specifications

3. **Employment Contract**
   - Role and responsibilities
   - Compensation and benefits
   - Working hours and location
   - Probation period
   - Additional terms and conditions

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `DATABASE_URL`: PostgreSQL connection string

### Database

The system uses PostgreSQL for storing:
- Generated contracts
- Contract templates
- Contract metadata and history

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
- Contract version control and history
- Payment integration (Stripe/PayPal)
- Contract analytics and reporting
- Automated contract renewal notifications

## ⚠️ Disclaimer

This is a tool to assist in contract creation but should not replace legal counsel. Always have important legal documents reviewed by qualified legal professionals.

## 🤝 Support

For support, please open an issue in the GitHub repository or contact the maintainers.
