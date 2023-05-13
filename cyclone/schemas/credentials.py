from pydantic import Field, BaseModel
from typing import Any
from enum import Enum

from .base import CycloneBaseModel


class CredentialsType(int, Enum):
    mailgun = 1
    sendgrid = 2


class Credentials(CycloneBaseModel):
    type: int = Field(
        description="The supported mail provider for the application", example=1
    )
    values: dict[str, Any] | None = Field(
        description="Relevant configuration values for the mail provider",
        example={
            "client_id": "xsf-440dkdd-djdj",
            "client_secret": "kdkdk-40djdkd-dkdkd",
        },
    )


class CredentialsUpdate(BaseModel):
    type: CredentialsType | None = Field(
        default=None,
        description="The supported mail provider for the application",
        example="mailgun",
    )
    values: dict[str, Any] | None = Field(
        default=None,
        description="Relevant configuration values for the mail provider",
        example={
            "client_id": "xsf-440dkdd-djdj",
            "client_secret": "kdkdk-40djdkd-dkdkd",
        },
    )
