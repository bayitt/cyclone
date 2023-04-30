from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


class CycloneBaseModel(BaseModel):
    uuid: UUID = Field(description="Unique identifier for the resource")
    created_at: datetime = Field(
        description="Timestamp at which the resource was created"
    )
    updated_at: datetime = Field(
        description="Timestamp at which the resource was last updated"
    )

    class Config:
        orm_mode = True
