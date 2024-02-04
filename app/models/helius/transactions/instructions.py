from typing import Optional
from pydantic import BaseModel, Field

class InnerInstruction(BaseModel):
    """
    Inner instructions for each instruction  # noqa: E501
    """
    accounts: Optional[list[str]] = None
    data: Optional[str] = None
    program_id: Optional[str] = Field(None, alias="programId")

class Instruction(BaseModel):
    """
    Individual instruction data in a transaction.  # noqa: E501
    """
    accounts: Optional[list[str]] = Field(None, description="The accounts used in instruction.")
    data: Optional[str] = Field(None, description="Data passed into the instruction")
    program_id: Optional[str] = Field(None, alias="programId", description="Program used in instruction")
    inner_instructions: Optional[list[InnerInstruction]] = Field(None, alias="innerInstructions", description="Inner instructions used in instruction")