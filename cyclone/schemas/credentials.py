from pydantic import Field
from typing import Any

from .base import CycloneBaseModel


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
