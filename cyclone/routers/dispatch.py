from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Annotated
from uuid import UUID
from math import ceil

from ..dependencies.application import application_by_uuid_pipe
from ..dependencies.database import get_db
from ..database.models import Dispatch
from ..schemas.dispatch import PaginatedDispatches

router = APIRouter()


@router.get("/", dependencies=[Depends(application_by_uuid_pipe)])
def get_dispatches(
    application_uuid: UUID,
    db: Session = Depends(get_db),
    page: Annotated[
        int, Query(description="Paginated page of results to fetch", example=1)
    ] = 1,
    number: Annotated[
        int, Query(description="Number of dispatches to fetch", example=10)
    ] = 10,
) -> PaginatedDispatches:
    skip = (page - 1) * number
    dispatches = (
        db.query(Dispatch)
        .filter(Dispatch.application_uuid == application_uuid)
        .offset(skip)
        .limit(number)
        .all()
    )

    totalDispatches = db.query(
        func.count(Dispatch.application_uuid == application_uuid)
    ).scalar()
    maxPages = ceil(totalDispatches / number)

    return {"currentPage": page, "maxPages": maxPages, "dispatches": dispatches}
