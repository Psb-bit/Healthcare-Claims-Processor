# tests/test_main.py

# Import FastAPI's test client to simulate HTTP requests to our app during testing
from fastapi.testclient import TestClient  

# Import the FastAPI app instance from the main module so we can test it
from app.main import app                   

# Initialize the test client using the FastAPI app instance
client = TestClient(app)  # client is now ready to make simulated HTTP requests to the app


# ------------------------------
# ✅ Test creating a valid claim
# ------------------------------
def test_create_valid_claim():
    # Simulate a POST request to the "/claims" endpoint with valid JSON data
    response = client.post("/claims", json={
        "claimant_name": "Test User",  # Name of the claimant
        "amount": 123.45,              # Amount of the claim
        "status": "submitted"          # Initial status of the claim
    })

    # Assert that the response status code is 200 (OK), indicating success
    assert response.status_code == 200  
    
    # Parse the response JSON data into a Python dictionary
    data = response.json()
    
    # Assert that the returned data matches the input values
    assert data["claimant_name"] == "Test User"  # Check if the name matches
    assert data["amount"] == 123.45              # Check if the amount matches
    assert data["status"] == "submitted"         # Check if the status matches

    # Capture the ID of the created claim for use in other tests
    global created_claim_id
    created_claim_id = data["id"]  # Save the ID of the created claim


# --------------------------------------
# ❌ Test creating a claim with bad input
# --------------------------------------
def test_create_invalid_claim():
    # Simulate a POST request with missing a required field ('amount')
    response = client.post("/claims", json={
        "claimant_name": "Incomplete",  # Name provided but no amount
        "status": "pending"             # Status provided
    })

    # Assert that FastAPI responds with a validation error (HTTP 422 Unprocessable Entity)
    assert response.status_code == 422


# --------------------------------------
# ✅ Test retrieving all claims
# --------------------------------------
def test_get_all_claims():
    # Simulate a GET request to the "/claims" endpoint to fetch all claims
    response = client.get("/claims")
    
    # Assert that the response status code is 200 (OK), indicating the request was successful
    assert response.status_code == 200
    
    # Assert that the response is a list (because we expect an array of claims)
    assert isinstance(response.json(), list)  # Should return a list of claims


# --------------------------------------------------
# ✅ Test retrieving a claim by ID (happy path)
# --------------------------------------------------
def test_get_claim_by_valid_id():
    # Simulate a GET request to retrieve a claim by its ID
    response = client.get(f"/claims/{created_claim_id}")
    
    # Assert that the status code is 200 (OK), indicating the request was successful
    assert response.status_code == 200
    
    # Parse the response JSON into a Python dictionary
    data = response.json()
    
    # Assert that the returned claim data matches the created claim ID
    assert data["id"] == created_claim_id
    assert data["claimant_name"] == "Test User"  # Verify the name of the claimant


# -----------------------------------------------------
# ❌ Test retrieving a claim by non-existing ID (error)
# -----------------------------------------------------
def test_get_claim_by_invalid_id():
    # Simulate a GET request to retrieve a claim by a non-existing ID (999999)
    response = client.get("/claims/999999")
    
    # Assert that the response status code is 404 (Not Found), since the claim doesn't exist
    assert response.status_code == 404       

    # Assert that the response contains a 'detail' field indicating the claim was not found
    assert response.json()["detail"] == "Claim not found"


# -------------------------------------
# ✅ Test updating a claim successfully
# -------------------------------------
def test_update_valid_claim():
    # Prepare the data to update the claim
    updated_data = {
        "claimant_name": "Updated User",  # New claimant name
        "amount": 999.99,                 # New claim amount
        "status": "approved"              # New claim status
    }

    # Simulate a PUT request to update the claim with the given ID
    response = client.put(f"/claims/{created_claim_id}", json=updated_data)
    
    # Assert that the response status code is 200 (OK), indicating the request was successful
    assert response.status_code == 200
    
    # Parse the response JSON into a Python dictionary
    data = response.json()
    
    # Assert that the returned claim data matches the updated values
    assert data["claimant_name"] == "Updated User"
    assert data["amount"] == 999.99
    assert data["status"] == "approved"


# ---------------------------------------
# ❌ Test updating a claim with bad input
# ---------------------------------------
def test_update_claim_invalid_input():
    # Prepare the data with missing the 'amount' field (invalid input)
    updated_data = {
        "claimant_name": "Oops",  # New name
        "status": "updated"       # New status, but no amount
    }

    # Simulate a PUT request to update the claim with missing 'amount'
    response = client.put(f"/claims/{created_claim_id}", json=updated_data)
    
    # Assert that the response status code is 422 (Unprocessable Entity), indicating validation failure
    assert response.status_code == 422  # Validation error from FastAPI


# ------------------------------------------------
# ❌ Test updating a non-existent claim (not found)
# ------------------------------------------------
def test_update_nonexistent_claim():
    # Prepare the data to update a non-existent claim
    updated_data = {
        "claimant_name": "Ghost",    # New name
        "amount": 1.0,               # New amount
        "status": "denied"           # New status
    }

    # Simulate a PUT request to update a claim with a non-existing ID (999999)
    response = client.put("/claims/999999", json=updated_data)
    
    # Assert that the response status code is 404 (Not Found), since the claim does not exist
    assert response.status_code == 404
    
    # Assert that the response contains a 'detail' field indicating the claim was not found
    assert response.json()["detail"] == "Claim not found"


# -----------------------------------
# ✅ Test deleting a claim by valid ID
# -----------------------------------
def test_delete_claim():
    # Simulate a DELETE request to remove the claim with the given ID
    response = client.delete(f"/claims/{created_claim_id}")
    
    # Assert that the response status code is 200 (OK), indicating the claim was deleted
    assert response.status_code == 200
    
    # Assert that the response contains a message confirming the deletion
    assert response.json()["message"] == "Claim deleted successfully"

    # Double-check that the claim no longer exists by trying to fetch it again
    response_check = client.get(f"/claims/{created_claim_id}")
    
    # Assert that the response status code is 404 (Not Found), as the claim was deleted
    assert response_check.status_code == 404


# -------------------------------------
# ❌ Test deleting a claim that doesn’t exist
# -------------------------------------
def test_delete_nonexistent_claim():
    # Simulate a DELETE request to remove a claim with a non-existing ID (999999)
    response = client.delete("/claims/999999")
    
    # Assert that the response status code is 404 (Not Found), since the claim doesn't exist
    assert response.status_code == 404
    
    # Assert that the response contains a 'detail' field indicating the claim was not found
    assert response.json()["detail"] == "Claim not found"
