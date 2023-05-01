from pydantic import BaseModel, Field, constr
from typing import Any

from .base import CycloneBaseModel
from .credentials import  Credentials


class ApplicationCreate(BaseModel):
    name: constr(to_lower=True) = Field(description="Name of the application")
    credentials_type: constr(to_lower=True) = Field(
        description="The supported mail provider for the application"
    )
    credentials_values: dict[str, Any] = Field(
        default=None, description="Relevant configuration values for the mail provider"
    )


class ApplicationUpdate(BaseModel):
    name: constr(to_lower=True) | None = Field(description="Name of the application")
    credentials_type: constr(to_lower=True) = Field(
        description="The supported mail provider for the application"
    )
    credentials_values: dict[str, Any] | None = Field(
        description="Relevant configuration values for the mail provider"
    )
    layout: str | None = Field(
        description="Layout/framework for mail templates used by the application"
    )


class Application(CycloneBaseModel):
    name: str = Field(description="Name of the application")
    api_key: str | None = Field(
        description="API Key for the application through which its emails are authenticated"
    )
    layout: str | None = Field(
        description="Layout/framework for mail templates used by the application"
    )
    credentials: Credentials = Field(
        description="Relevant mail credentials for the application"
    )
