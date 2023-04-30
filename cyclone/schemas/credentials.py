from pydantic import Field
from enum import Enum
from typing import Any

from .base import CycloneBaseModel


class CredentialsType(str, Enum):
    mailgun = 1


class Credentials(CycloneBaseModel):
    type: CredentialsType = Field(
        description="The supported mail provider for the application"
    )
    values: dict[str, Any] | None = Field(
        description="Relevant configuration values for the mail provider"
    )
