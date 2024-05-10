from datetime import date
from typing import Optional
from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass

class User(Base):
    '''User model'''
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    email: Mapped[str] = mapped_column(String())
    password: Mapped[str] = mapped_column(String())

class Card(Base):
    '''User model'''
    __tablename__ = "card"
    id: Mapped[int] = mapped_column(primary_key=True)
    card_number: Mapped[int] = mapped_column(Integer())
    batch_number: Mapped[Optional[str]] = mapped_column(String())
    batch_date: Mapped[Optional[date]] = mapped_column(Date())
    batch_name: Mapped[Optional[str]] = mapped_column(String())
    batch_position: Mapped[Optional[int]] = mapped_column(Integer())
