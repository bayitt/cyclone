from pydantic import Field, constr
from enum import Enum
from typing import Any

from .base import CycloneBaseModel

class Credentials(CycloneBaseModel):
    type: int = Field(
        description="The supported mail provider for the application"
    )
    values: dict[str, Any] | None = Field(
        description="Relevant configuration values for the mail provider"
    )
