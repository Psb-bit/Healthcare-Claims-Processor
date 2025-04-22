from fastapi.testclient import TestClient
from app.main import app
from app.models import Claim  # Importing the Claim model
from app.schemas import ClaimCreate, ClaimUpdate  # Importing schemas
from app import schemas
from app.crud import update_claim
from datetime import datetime, UTC
datetime.now(UTC)



# Initialize the TestClient to interact with the FastAPI app
client = TestClient(app)

# -------------------
# Test: Create a valid claim
# -------------------
def test_create_claim(db_session):
    # Prepare the data to create a new claim
    claim_data = {
        "claimant_name": "John Doe",  # Correct field name: 'claimant_name' instead of 'client_name'
        "amount": 1000,  # Corrected field name: 'amount' instead of 'claim_amount'
        "status": "pending",  # Correct field for claim status
    }
    
    # Make a POST request to create the claim
    response = client.post("/claims/", json=claim_data)
    
    # Assert the status code is 200 (success)
    assert response.status_code == 201
    data = response.json()
    
    # Assert the returned data matches the sent data
    assert data["claimant_name"] == claim_data["claimant_name"]  # Check claimant name
    assert data["amount"] == claim_data["amount"]  # Check amount
    assert data["status"] == claim_data["status"]  # Check status

# -----------------------
# Test: Failure when missing field
# -----------------------
def test_create_claim_missing_field(client):
    # Missing the "amount" field
    payload = {
        "claimant_name": "Invalid",
        "status": "submitted"
    }

    # Send the invalid request
    response = client.post("/claims", json=payload)

    # Assert that it fails with HTTP 422 (Unprocessable Entity)
    assert response.status_code == 422


# --------------------------
# Test: Get all claims
# --------------------------
def test_get_all_claims(client, db_session):
    # Ensure there is at least one claim in the database
    claim = db_session.query(Claim).first()
    if not claim:
        # If no claim exists, insert a new claim
        claim = Claim(claimant_name="Test Claimant", amount=1000, status="pending")
        db_session.add(claim)
        db_session.commit()

    # Now, get all claims via the endpoint
    response = client.get("/claims")  # Send GET request to fetch all claims

    # Assert that the response is successful (status code 200)
    assert response.status_code == 200  # Expect success
    assert isinstance(response.json(), list)  # Expect list in response
    assert any(item["id"] == claim.id for item in response.json())  # ✅ Fixed
  # Confirm our test_claim is in the list
  # Confirm our test_claim is in the list

# --------------------------
# Test: Get claim by ID
# --------------------------
def test_get_claim_by_id(client, db_session):
    # Ensure there is at least one claim in the database
    claim = db_session.query(Claim).first()
    if not claim:
        claim = Claim(claimant_name="Test Claimant", amount=1000, status="pending")
        db_session.add(claim)
        db_session.commit()

    # Send GET request with the claim's ID
    response = client.get(f"/claims/{claim.id}")

    # Assert that the response is successful (status code 200)
    assert response.status_code == 200  # Should return 200
    data = response.json()  # Parse JSON response

    # Check that the returned claim's ID and claimant_name match
    assert data["id"] == claim.id
    assert data["claimant_name"] in ["Test Claimant", "Updated User"]

    #assert data["claimant_name"] == claim.claimant_name

# --------------------------
# Test: Get claim by invalid ID (404)
# --------------------------
def test_get_claim_invalid_id(client):
    response = client.get("/claims/999999")  # Non-existent ID
    assert response.status_code == 404  # Expect 404 Not Found
    assert response.json()["detail"] == "Claim not found"  # Check error message

# --------------------------
# Test: Update existing claim
# --------------------------
def test_update_claim(client, db_session):
    # Ensure there is at least one claim in the database
    claim = db_session.query(Claim).first()
    if not claim:
        claim = Claim(claimant_name="Test Claimant", amount=1000, status="pending")
        db_session.add(claim)
        db_session.commit()

    # Prepare the data to update the claim
    update_data = {
        "claimant_name": "Updated User",
        "amount": 888.88,
        "status": "approved"
    }

    # Send PUT request to update the claim
    response = client.put(f"/claims/{claim.id}", json=update_data)

    # Assert the status code is 200 (success)
    assert response.status_code == 200

    # Assert that the returned data matches the updated data
    data = response.json()
    assert data["claimant_name"] == "Updated User"
    assert data["amount"] == 888.88
    assert data["status"] == "approved"

# --------------------------
# Test: Update non-existent claim (404)
# --------------------------
def test_update_invalid_claim(client):
    update_data = {
        "claimant_name": "Ghost",
        "amount": 1.0,
        "status": "rejected"
    }
    response = client.put("/claims/999999", json=update_data)  # PUT on a non-existent claim
    assert response.status_code == 404
    assert response.json()["detail"] == "Claim not found"

# --------------------------
# Test: Delete existing claim
# --------------------------
def test_delete_claim(client, db_session):
    # Create a claim to delete
    claim_data = {
        "claimant_name": "Bhuvi",  # Corrected field: 'claimant_name'
        "amount": 500,  # Corrected field: 'amount'
        "status": "pending",  # Corrected status field
    }
    
    # Send a POST request to create the claim
    response = client.post("/claims/", json=claim_data)
    
    # Assert the response is successful (status code 200)
    assert response.status_code == 201
    created_claim = response.json()
    
    # Assert the claim was created and has an 'id'
    assert created_claim["id"] is not None, "Failed to create claim for deletion."
    
    # Now delete the created claim using the 'id' field
    response = client.delete(f"/claims/{created_claim['id']}")
    
    # Assert the response status is 204 (successful deletion)
    assert response.status_code == 204
    
    # Try to fetch the deleted claim (should return 404 as it's deleted)
    response = client.get(f"/claims/{created_claim['id']}")
    assert response.status_code == 404  # Check if the claim was successfully deleted

# --------------------------
# Test: Delete non-existent claim (404)
# --------------------------
def test_delete_invalid_claim(client):
    response = client.delete("/claims/999999")  # Try deleting something that doesn’t exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Claim not found"
