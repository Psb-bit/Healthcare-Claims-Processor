# Healthcare-Claims-Processor

A FastAPI application that allows users to create, update, delete, and view claims in the healthcare industry. The system uses PostgreSQL as the database and SQLAlchemy for ORM. This project also includes unit and integration tests.

## Features:
- Create new healthcare claims
- Retrieve all claims or specific claims by ID
- Update an existing claim
- Delete claims from the system

## Installation

To set up the project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/Psb-bit/Healthcare-Claims-Processor.git

2. Navigate into the project directory:
  cd Healthcare-Claims-Processor

3. Create a virtual environment
  python -m venv venv

4. Activate the virtual environment:

  On Windows:
    .\venv\Scripts\activate
  On macOS/Linux:
    source venv/bin/activate
    
5. Install the required dependencies:
  pip install -r requirements.txt

6. Set up the database (if applicable). You might need to run a migration or setup script depending on your setup.

7. Run the application:
  uvicorn app.main:app --reload
8. Access the app at http://localhost:8000.

## Usage

## Endpoints

- `POST /claims/` - Create a new claim
- `GET /claims/{claim_id}/` - Get a claim by ID
- `PUT /claims/{claim_id}/` - Update a claim
- `DELETE /claims/{claim_id}/` - Delete a claim
- `GET /claims/` - Get all claims

Example cURL command to create a new claim:
curl -X 'POST' \
  'http://localhost:8000/claims/' \
  -H 'Content-Type: application/json' \
  -d '{
  "claimant_name": "John Doe",
  "amount": 1500,
  "status": "pending"
}'


## Running Tests
You can run the tests using pytest:
    pytest
The tests will run automatically during GitHub Actions CI after each push to the repository.

GitHub Actions CI
This project includes a GitHub Actions configuration to automatically run tests on every push to the repository. The tests are run in a continuous integration pipeline to ensure code quality.

## Directory Structure
Healthcare-Claims-Processor/
├── app/
│   ├── __init__.py              # Application initialization
│   ├── main.py                  # FastAPI entry point
│   ├── models.py                # SQLAlchemy models
│   ├── schemas.py               # Pydantic schemas
│   ├── crud.py                  # Business logic (CRUD operations)
│   ├── database.py              # PostgreSQL connection and session management
├── tests/
│   ├── __init__.py              # Test initialization
│   ├── test_crud_unit.py        # Unit tests using MagicMock
│   ├── test_crud_integration.py # Integration tests with a test database
│   ├── conftest.py              # Pytest fixtures for shared test setup
│   ├── test_main.py             # FastAPI app tests
├── requirements.txt             # Project dependencies
└── README.md                    # You're reading it!


## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your proposed changes.
Make sure to write tests for new features and fix any failing tests.

## License 
This project is licensed under the MIT License - see the LICENSE file for details.
