from pydantic import BaseModel, Field
from typing import Any


class DispatchCreate(BaseModel):
    email: str = Field(
        description="Unique identifier for the email to be sent", example="VERIFY_USER"
    )
    variables: dict[str, Any] | None = Field(
        default=None,
        description="Variables to be sent along with the email",
        example={"name": "James Jackson", "token": "uvbfjkdld-didjd8d-ddmd89"},
    )
