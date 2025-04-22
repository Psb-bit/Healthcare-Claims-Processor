# # Entry point (FastAPI app lives here)

# from fastapi import FastAPI

# app = FastAPI()

# @app.get("/")
# def read_root():
#     return {"message": "Healthcare Claims API is up and running!"}



# #This will tell SQLAlchemy to create the claims table inside your claims_db.just once to create table.
# from .database import Base, engine
# from .models import Claim

# Base.metadata.create_all(bind=engine)

# Import necessary libraries and modules for the FastAPI application

from fastapi import FastAPI, Depends, HTTPException,Body, status  # FastAPI framework for building the API, dependency injection, and HTTP exception handling
from sqlalchemy.orm import Session  # SQLAlchemy's Session object for interacting with the database
from . import models, schemas, crud  # Import the models (ORM), schemas (Pydantic validation), and CRUD functions
from app.database import SessionLocal, engine  # Import the database session creator and engine for connecting to the DB



# Create all tables in the database if they don't exist yet. This ensures that the DB schema is updated based on the models defined in 'models.py'.
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application instance
app = FastAPI()

# Dependency function to get a new DB session per request.
def get_db():
    """
    This function ensures that a new database session is created for each request,
    and that it is closed after the request has been processed.
    """
    db = SessionLocal()  # Open a new session using the SessionLocal object (defined in database.py)
    try:
        yield db  # Yield the session to be used in the route functions
    finally:
        db.close()  # Close the session after the request is handled to release the connection


# -------------------------------------
# POST route to create a new claim
# -------------------------------------
@app.post("/claims", response_model=schemas.Claim, status_code=201)  # The route handles POST requests at /claims and expects a 'Claim' schema as the response.
def create_claim(claim: schemas.ClaimCreate, db: Session = Depends(get_db)):  # Accept claim data from the request and inject the DB session
    """
    This endpoint creates a new claim in the database.
    """
    # Call the 'create_claim' function from 'crud.py', passing in the DB session and the claim data to create a new record.
    return crud.create_claim(db=db, claim=claim)  # Return the created claim object


# -------------------------------------
# GET route to fetch all claims
# -------------------------------------
@app.get("/claims", response_model=list[schemas.Claim])  # The route handles GET requests at /claims and returns a list of claims.
def read_claims(db: Session = Depends(get_db)):  # This route gets a DB session injected
    """
    This endpoint fetches all claims stored in the database.
    """
    # Call the 'get_all_claims' function from 'crud.py' to retrieve all claims.
    return crud.get_all_claims(db)  # Return the list of claims


# -------------------------------------
# GET route to fetch a single claim by ID
# -------------------------------------
@app.get("/claims/{claim_id}", response_model=schemas.Claim)  # Route accepts a claim_id in the URL path and returns a single claim object.
def read_claim(claim_id: int, db: Session = Depends(get_db)):  # 'claim_id' is a path parameter
    """
    This endpoint fetches a specific claim by its ID.
    """
    # Fetch the claim from the database using 'crud.get_claim_by_id' by passing the DB session and claim ID.
    db_claim = crud.get_claim_by_id(db, claim_id)
    
    # If no claim is found, raise an HTTPException with a 404 status code (Not Found).
    if db_claim is None:  # If the claim is not found, return a 404 error.
        raise HTTPException(status_code=404, detail="Claim not found")  
    
    # If the claim is found, return it as a response.
    return db_claim


# -------------------------------------
# PUT route to update an existing claim by ID
# -------------------------------------
@app.put("/claims/{claim_id}", response_model=schemas.Claim)  # Route to update a specific claim by ID.
def update_claim(
    claim_id: int,  # Path parameter: the ID of the claim to be updated.
    updated_claim: schemas.ClaimCreate,  # Request body: contains new claim data, validated with ClaimCreate schema.
    db: Session = Depends(get_db)  # Inject a DB session using FastAPI's dependency system.
):
    """
    This endpoint updates a claim with the given claim ID using new data provided in the request body.
    """

    # Fetch the claim from the database using the provided claim ID.
    db_claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()

    # If no claim is found with the given ID, raise a 404 Not Found error.
    if db_claim is None:
        raise HTTPException(status_code=404, detail="Claim not found")

    # Validate that the status provided is one of the allowed Enum values.
    if updated_claim.status not in [status.value for status in schemas.ClaimStatus]:
        raise HTTPException(status_code=400, detail="Invalid status value")

    # Update fields with the data received from the request.
    db_claim.claimant_name = updated_claim.claimant_name
    db_claim.amount = updated_claim.amount
    db_claim.status = updated_claim.status  # Assign a valid Enum value (as string).

    # Save the updated claim to the database.
    db.commit()

    # Refresh the claim instance to reflect updated DB state.
    db.refresh(db_claim)

    # Return the updated claim, which will be serialized using the Claim schema.
    return db_claim


@app.delete("/claims/{claim_id}", status_code=204)  
# This line defines a DELETE HTTP route at the path "/claims/{claim_id}".
# When a DELETE request is made to this path (e.g., /claims/5), this function will be called.
# 'status_code=204' tells FastAPI to return a 204 No Content response if successful (no body in the response).

def delete_claim(claim_id: int, db: Session = Depends(get_db)):  
    # This is the route handler function.
    # 'claim_id: int' is a path parameter extracted from the URL.
    # 'db: Session = Depends(get_db)' injects a database session using FastAPI's dependency system.
    # 'Depends(get_db)' means FastAPI will automatically call the 'get_db' function and pass its result here.

    db_claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()  
    # This line queries the database to find a claim with the given claim_id.
    # 'db.query(models.Claim)' creates a query for the Claim table.
    # '.filter(models.Claim.id == claim_id)' filters records where 'id' matches the path parameter.
    # '.first()' returns the first match or None if not found.

    if db_claim is None:  
        # If no claim was found (i.e., claim_id doesn't exist), then:
        raise HTTPException(status_code=404, detail="Claim not found")  
        # Raise an HTTP 404 Not Found error with a custom error message.
        # This stops the function and sends the error as the response.

    db.delete(db_claim)  
    # Delete the found claim object from the database session.
    # Note: It doesn't delete it in the database yet — it just marks it for deletion.

    db.commit()  
    # Commits the current transaction, which includes the deletion of the claim.
    # Now the claim is permanently removed from the database.

    return  
    # Return nothing. Since the route is defined with 'status_code=204',
    # FastAPI will return an empty response with HTTP 204 status (No Content).


