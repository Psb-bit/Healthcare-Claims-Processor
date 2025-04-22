# Pydantic schemas (for request/response)
# Importing BaseModel from Pydantic to define request/response schemas

# Import necessary modules from Pydantic for data validation
from pydantic import BaseModel,  Field, field_validator, validator, ConfigDict

# Optional type hint and Enum class for restricting field values
from typing import Optional
from enum import Enum

# For handling timestamps like 'submitted_at'
from datetime import datetime
from datetime import datetime, UTC
datetime.now(UTC)



# Define an Enum class to restrict the allowed values for status
class ClaimStatus(str, Enum):
    submitted = "submitted"
    approved = "approved"
    rejected = "rejected"
    pending = "pending"
    closed = "closed"


# Base schema used for both creation and update
class ClaimBase(BaseModel):
    # claimant_name is required, must have at least 1 character
    claimant_name: str = Field(..., min_length=1, description="Name of the claimant (required)")

    # amount is required, must be a float greater than 0
    amount: float = Field(..., gt=0, description="Claim amount must be greater than 0")

    # status must be one of the values defined in ClaimStatus Enum
    status: ClaimStatus = Field(..., description="Claim status")

    # Custom validator to ensure claimant_name is not empty or just spaces
    @field_validator('claimant_name')
    def name_cannot_be_empty(cls, value):
        if not value.strip():
            raise ValueError('Claimant name cannot be empty or just spaces')
        return value


# Schema used when creating a new claim – inherits from ClaimBase
class ClaimCreate(ClaimBase):
    pass  # No additional fields needed, just reuse base fields


# Schema used when updating an existing claim – also inherits from ClaimBase
class ClaimUpdate(ClaimBase):
    pass  # Reuse base fields for updates too


# Schema for returning a full claim, including the auto-generated ID and submitted timestamp
class Claim(ClaimBase):
    id: int  # Auto-generated ID
    submitted_at: datetime  # Timestamp when the claim was submitted

    # orm_mode allows Pydantic to read data from SQLAlchemy model instances
    class Config:
        model_config = ConfigDict(from_attributes=True)
        #form_attributes = True
        #orm_mode = True
