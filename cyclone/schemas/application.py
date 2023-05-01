from pydantic import BaseModel, Field, constr
from typing import Any

from .base import CycloneBaseModel
from .credentials import Credentials


class ApplicationCreate(BaseModel):
    name: constr(to_lower=True) = Field(
        description="Name of the application", example="maui"
    )
    credentials_type: constr(to_lower=True) = Field(
        description="The supported mail provider for the application", example="mailgun"
    )
    credentials_values: dict[str, Any] = Field(
        default=None,
        description="Relevant configuration values for the mail provider",
        example={
            "client_id": "xsf-440dkdd-djdj",
            "client_secret": "kdkdk-40djdkd-dkdkd",
        },
    )


class ApplicationUpdate(BaseModel):
    name: constr(to_lower=True) | None = Field(description="Name of the application")
    credentials_type: constr(to_lower=True) = Field(
        description="The supported mail provider for the application", example="mailgun"
    )
    credentials_values: dict[str, Any] | None = Field(
        description="Relevant configuration values for the mail provider",
        example={
            "client_id": "xsf-440dkdd-djdj",
            "client_secret": "kdkdk-40djdkd-dkdkd",
        },
    )
    layout: str | None = Field(
        description="Layout/framework for mail templates used by the application"
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
