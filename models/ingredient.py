from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

from models.base import Base


class Ingredient(Base):
    __tablename__ = "ingredients"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))