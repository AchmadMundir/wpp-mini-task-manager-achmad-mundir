from datetime import datetime

from sqlalchemy import BigInteger, CheckConstraint, DateTime, Identity, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Board(Base):
    __tablename__ = "boards"
    __table_args__ = (
        CheckConstraint("char_length(trim(name)) > 0", name="ck_boards_name_not_blank"),
    )

    id: Mapped[int] = mapped_column(BigInteger, Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )

    tasks: Mapped[list["Task"]] = relationship(  # noqa: F821
        back_populates="board",
        passive_deletes=True,
    )

