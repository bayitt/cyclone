from pydantic import BaseModel, Field
from typing import Any

from .base import CycloneBaseModel


class DispatchCreate(BaseModel):
    email: str = Field(
        description="Unique identifier for the email to be sent", example="VERIFY_USER"
    )
    recipients: list[str] = Field(
        description="Person or people to receive the email",
        example=["jjackson@gmail.com"],
    )
    variables: dict[str, Any] | None = Field(
        default=None,
        description="Variables to be sent along with the email",
        example={"name": "James Jackson", "token": "uvbfjkdld-didjd8d-ddmd89"},
    )


class DispatchEmail(BaseModel):
    name: str = Field(description="Name of the email", example="VERIFY_USER")

    class Config:
        orm_mode = True


class Dispatch(CycloneBaseModel):
    template: str = Field(
        description="Email template sent to the recipients", example=""
    )
    variables: dict[str, Any] | None = Field(
        default=None,
        description="Variables sent along with the email",
        example={"name": "James Jackson", "token": "uvbfjkdld-didjd8d-ddmd89"},
    )
    logs: str | None = Field(
        default=None,
        description="Recorded logs for the dispatch containing information about the dispatch failing",
    )
    email: DispatchEmail = Field(description="Associated email model for the dispatch")


class PaginatedDispatches(BaseModel):
    currentPage: int = Field(
        description="Current page of dispatches being returned", example=1
    )
    maxPages: int = Field(
        description="Maximum number of paginated pages based on the passed in page query parameter",
        example=10,
    )
    dispatches: list[Dispatch] = Field(description="Dispatches being returned")
