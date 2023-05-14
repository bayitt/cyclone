from pydantic import BaseModel, Field

from .base import CycloneBaseModel


class EmailCreate(BaseModel):
    name: str = Field(description="Name of the email", example="VERIFY_USER")
    template: str = Field(description="Specific template for the email")
    variables: list[str] | None = Field(
        default=None,
        description="Variables for the email template",
        example=["order", "timestamp", "key"],
    )


class EmailUpdate(BaseModel):
    name: str | None = Field(
        default=None, description="Name of the email", example="VERIFY_USER"
    )
    template: str | None = Field(
        default=None, description="Specific template for the email"
    )
    variables: list[str] | None = Field(
        default=None,
        description="Variables for the email template",
        example=["order", "timestamp", "key"],
    )


class Email(CycloneBaseModel):
    name: str = Field(description="Name of the email", example="VERIFY_USER")
    template: str = Field(description="Specific template for the email")
    variables: list[str] | None = Field(
        default=None,
        description="Variables for the email template",
        example=["order", "timestamp", "key"],
    )
