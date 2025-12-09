from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from db_connection import Base


class User(Base):
    __table_args__ = {"schema": "dbo"}
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
