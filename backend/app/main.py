import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Annotated, Literal
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.concurrency import run_in_threadpool

from app.database import engine, get_session, init_database
from app.models import Click
from app.schemas import ClickResponse


logger: logging.Logger = logging.getLogger(__name__)

BRAND_URL: str = "https://www.dell.com/"

DatabaseSession = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    try:
        await run_in_threadpool(init_database)
        yield
    finally:
        await run_in_threadpool(engine.dispose)


app: FastAPI = FastAPI(
    title="Brand Click Tracker",
    lifespan=lifespan,
)


@app.get("/click", status_code=302, response_class=RedirectResponse)
def track_click(
    request: Request,
    session: DatabaseSession,
    offer: Annotated[Literal["Dell"], Query()],
    sub1: Annotated[str, Query()],
) -> RedirectResponse:
    click: Click = Click(
        click_id=uuid4(),
        offer=offer,
        sub1=sub1,
        timestamp=datetime.now(timezone.utc),
        ip=request.client.host if request.client else "",
        user_agent=request.headers.get("user-agent", ""),
    )

    try:
        session.add(click)
        # Подтверждаем запись до редиректа.
        session.commit()
    except SQLAlchemyError:
        session.rollback()
        logger.error("Не удалось сохранить клик")
        raise HTTPException(
            status_code=503,
            detail="Не удалось сохранить клик. Попробуйте позже.",
        ) from None

    return RedirectResponse(
        url=BRAND_URL,
        status_code=302,
        headers={"Cache-Control": "no-store"},
    )


@app.get("/clicks", response_model=list[ClickResponse])
def get_clicks(session: DatabaseSession) -> list[Click]:
    statement = select(Click).order_by(
        Click.timestamp,
        Click.click_id,
    )

    return list(session.scalars(statement).all())