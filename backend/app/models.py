from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, Text, Uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Click(Base):
    __tablename__ = "clicks"

    click_id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    offer: Mapped[str] = mapped_column(Text, nullable=False)
    sub1: Mapped[str] = mapped_column(Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    ip: Mapped[str] = mapped_column(Text, nullable=False)
    user_agent: Mapped[str] = mapped_column(Text, nullable=False)