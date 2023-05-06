from pydantic import BaseModel, Field
from typing import Any

from .base import CycloneBaseModel
from .credentials import CredentialsType, Credentials


class ApplicationCreate(BaseModel):
    name: str = Field(description="Name of the application", example="maui")
    credentials_type: CredentialsType = Field(
        description="The supported mail provider for the application", example="mailgun"
    )
    credentials_values: dict[str, Any] | None = Field(
        default=None,
        description="Relevant configuration values for the mail provider",
        example={
            "client_id": "xsf-440dkdd-djdj",
            "client_secret": "kdkdk-40djdkd-dkdkd",
        },
    )


class ApplicationUpdate(BaseModel):
    name: str | None = Field(default=None, description="Name of the application")
    credentials_type: CredentialsType | None = Field(
        default=None,
        description="The supported mail provider for the application",
        example="mailgun",
    )
    credentials_values: dict[str, Any] | None = Field(
        default=None,
        description="Relevant configuration values for the mail provider",
        example={
            "client_id": "xsf-440dkdd-djdj",
            "client_secret": "kdkdk-40djdkd-dkdkd",
        },
    )
    layout: str | None = Field(
        default=None,
        description="Layout/framework for mail templates used by the application",
    )


class Application(CycloneBaseModel):
    name: str = Field(description="Name of the application", example="maui")
    api_key: str | None = Field(
        description="API Key for the application through which its emails are authenticated",
        example="MJTDY-EIBQE_OTNTL_HKMFZ_JQNUS_HYPRD_MOUGT",
    )
    layout: str | None = Field(
        description="Layout/framework for mail templates used by the application"
    )
    credentials: Credentials = Field(
        description="Relevant mail credentials for the application"
    )
