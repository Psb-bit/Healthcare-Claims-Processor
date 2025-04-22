# CRUD operations for interacting with the Claim model (Create, Read, Update, Delete)

from sqlalchemy.orm import Session  # Import Session for interacting with the database
from . import models, schemas       # Import models and schemas for interacting with DB and validating data
from datetime import datetime, timezone

submitted_at = datetime.now(timezone.utc)

# Import datetime for working with timestamps

# -----------------------------
# Create a new claim in the database
# -----------------------------
def create_claim(db: Session, claim: schemas.ClaimCreate) -> models.Claim:
    """
    This function accepts a claim object, creates a new entry in the DB, and returns the newly created claim.
    """
    # Create a new Claim model instance by mapping fields from the schema to the model
    db_claim = models.Claim(
        claimant_name=claim.claimant_name,  # Map the 'client_name' from the schema to the model's 'claimant_name'
        amount=claim.amount,              # Map the 'amount' from the schema to the model's 'amount'
        status=claim.status.value,        # Convert Enum 'status' to its string value for the model
        submitted_at=datetime.utcnow()    # Set the current timestamp when the claim is created
    )
    
    # Add the newly created claim to the database session (staging it for commit)
    db.add(db_claim)  
    
    # Commit the changes to the database, which saves the new claim record
    db.commit()  
    
    # Refresh the db_claim instance to load DB-generated fields like 'id'
    db.refresh(db_claim)  
    
    # Return the newly created claim object with its 'id' and other fields
    return db_claim  


# -----------------------------
# Retrieve all claims from the database
# -----------------------------
# -----------------------------
# Retrieve all claims from the database
# -----------------------------
def get_all_claims(db: Session):
    """
    Fetch all claims from the 'claims' table and return them as a list.
    """
    # Perform a query on the 'Claim' table and fetch all rows (claims) from the database
    return db.query(models.Claim).all()  # 'all()' retrieves all rows in the table



# -----------------------------
# Retrieve a specific claim by ID
# -----------------------------
def get_claim_by_id(db: Session, claim_id: int):
    """
    Fetch a specific claim from the database by its ID.
    """
    # Query the 'Claim' table and filter it by 'id' to fetch a claim matching the given claim_id
    return db.query(models.Claim).filter(models.Claim.id == claim_id).first()  
    # '.filter()' applies a condition to filter results by the 'id' column
    # '.first()' returns the first result that matches or None if not found


# -----------------------------
# Update a claim in the database by its ID
# -----------------------------
def update_claim(db: Session, claim_id: int, updated_data: schemas.ClaimUpdate):
    """
    Update an existing claim in the database by its ID with the provided updated data.
    """
    # Query the 'Claim' table and filter by the claim's 'id' to find the claim to update
    db_claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()

    # Check if the claim was found in the database
    if db_claim:
        # Update the fields of the found claim using the provided updated data
        db_claim.claimant_name = updated_data.claimant_name  # Corrected: 'client_name' → 'claimant_name'
        db_claim.amount = updated_data.amount                # Set the 'amount' to the new value
        db_claim.status = updated_data.status.value          # Convert the Enum 'status' to a string and update
        db.commit()                                          # Save the changes to the database
        db.refresh(db_claim)                                 # Refresh the claim object to get updated data from DB

    # Return the updated claim (or None if not found)
    return db_claim

# -----------------------------
# Delete a claim by ID
# -----------------------------
def delete_claim(db: Session, claim_id: int):
    """
    Delete a claim from the database by its ID.
    """
    # Query the 'Claim' table and filter by 'id' to find the claim to delete
    db_claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()
    
    # Check if the claim was found in the database
    if db_claim:
        # If found, delete the claim from the session (marks it for deletion)
        db.delete(db_claim)  
        
        # Commit the changes to the database, which removes the claim permanently
        db.commit()  

    # Return the deleted claim (or None if not found)
    return db_claim  
