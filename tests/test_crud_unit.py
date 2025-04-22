# Importing pytest for writing unit tests
import pytest

# MagicMock is used to mock objects like database sessions and query results
from unittest.mock import MagicMock

# Importing the actual functions we want to test from our crud.py
from app import crud

# Importing our Pydantic schemas for creating and updating claim data
from app.schemas import ClaimCreate, ClaimUpdate

# Importing the SQLAlchemy model used in our application for consistency
from app.models import Claim


# ----------- Test for Creating a Claim -----------

def test_create_claim():
    # Create a mocked database session
    db = MagicMock()

    # Simulated claim creation input using Pydantic schema (must match schema field names)
    claim_data = ClaimCreate(
        claimant_name="Alice",
        amount=5000,
        status="pending",
        #claim_type="Medical"
    )

    # Call the actual CRUD function with the mocked DB and input
    result = crud.create_claim(db=db, claim=claim_data)

    # Verify that the returned object is an instance of our Claim model
    assert isinstance(result, Claim)

    # Check that data in the returned object matches the input
    assert result.claimant_name == "Alice"
    assert result.amount == 5000
    assert result.status == "pending"
    #assert result.claim_type == "Medical"


# ----------- Test for Getting a Claim by ID -----------

def test_get_claim():
    db = MagicMock()

    # Creating a fake claim that the DB would return
    mock_claim = Claim(
        id=1,
        claimant_name="Alice",
        amount=5000,
        status="pending",
        #claim_type="Medical"
    )

    # Mock the DB's query chain to return the fake claim
    db.query().filter().first.return_value = mock_claim

    # Call the function under test
    result = crud.get_claim_by_id(db=db, claim_id=1)

    # Assert that the returned claim is correct
    assert result.claimant_name == "Alice"
    assert result.amount == 5000
    assert result.status == "pending"


# ----------- Test for Updating a Claim -----------

def test_update_claim():
    db = MagicMock()

    # Simulate the existing claim in the DB
    existing_claim = Claim(
        id=1,
        claimant_name="Alice",
        amount=5000,
        status="pending",
        #claim_type="Medical"
    )

    # Mock the DB to return this existing claim
    db.query().filter().first.return_value = existing_claim

    # Input data to update (must match the ClaimUpdate schema)
    updated_claim_data = ClaimUpdate(
        claimant_name="Alice",
        amount=7000,            # Changed amount
        status="approved",      # Changed status
        #claim_type="Medical"
    )

    # Run the update function
    result = crud.update_claim(db=db, claim_id=1, updated_data=updated_claim_data)


    # Assertions to make sure updates were applied
    assert result.amount == 7000
    assert result.status == "approved"


# ----------- Test for Deleting a Claim -----------

def test_delete_claim():
    db = MagicMock()

    # Mock a claim object to be deleted
    mock_claim = Claim(
        id=1,
        claimant_name="Alice",
        amount=5000,
        status="pending",
        #claim_type="Medical"
    )

    # Configure mock DB to return the mock claim
    db.query().filter().first.return_value = mock_claim

    # Run delete function
    result = crud.delete_claim(db=db, claim_id=1)

    # Assert that the returned object is the deleted claim
    assert result == mock_claim

    # Also verify that delete and commit were called correctly
    db.delete.assert_called_once_with(mock_claim)
    db.commit.assert_called_once()


# ----------- Test for Getting All Claims -----------

def test_get_all_claims():
    db = MagicMock()

    # List of mock claims to simulate DB response
    mock_claims = [
        Claim(id=1, claimant_name="Alice", amount=5000, status="pending"), #,claim_type="Medical"),
        Claim(id=2, claimant_name="Bob", amount=10000, status="approved")#, claim_type="Life")
    ]

    # Set the DB query to return this list
    db.query().all.return_value = mock_claims

    # Call the function
    result = crud.get_all_claims(db=db)

    # Check that we got the full list
    assert len(result) == 2
    assert result[0].claimant_name == "Alice"
    assert result[1].claimant_name == "Bob"
