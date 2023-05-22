from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Annotated

from ..dependencies.application import application_by_uuid_pipe
from ..dependencies.database import get_db

router = APIRouter()


@router.get("/", dependencies=[Depends(application_by_uuid_pipe)])
def get_dispatches(
    db: Session = Depends(get_db),
    page: Annotated[
        int | None, Query(description="Paginated page of results to fetch", example=1)
    ] = 1,
    number: Annotated[
        int | None, Query(description="Number of dispatches to fetch", example=10)
    ] = 10,
):
    print("")
