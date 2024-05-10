from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.services.database_connection import DBConnection
from app.data.models import Card, User


class UsersRepository:
    def __init__(self):
        self.db = DBConnection()
        self.engine = self.db.engine

    def create_user(self, name: str, email: str, password: str):
        user = User(
            name=name,
            email=email,
            password=self.encrypt_password(password)
        )
        user_exists = self.get_user_by_email(user.email)
        if user_exists:
            return f"Error: user with email {user.email} already exists"
        with Session(self.engine) as session:
            session.add(user)
            session.commit()
        return "User created"

    def get_user_by_email(self, email: str):
        try:
            with Session(self.engine) as session:
                users = session.scalars(select(User).where(User.email == email))
                if users:
                    user = users.one()
                else:
                    return None
            return user
        except Exception as e:
            return None

    def get_by_id(self, id: int):
        try:
            with Session(self.engine) as session:
                users = session.scalars(select(User).where(User.id == id))
                if users:
                    user = users.one()
                else:
                    return None
            return user
        except Exception as e:
            return None

    def auth_user(self, email: str, password: str):
        user = self.get_user_by_email(email)
        if not user or not check_password_hash(user.password, password):
            return None
        return user

    def encrypt_password(self, password: str):
        return generate_password_hash(password)


class CardsRepository:
    def __init__(self):
        self.db = DBConnection()
        self.engine = self.db.engine

    def create_card(
        self,
        card_number: int,
        batch_number: str = None,
        batch_date: date = None,
        batch_name: str = None,
        batch_position: int = None,
    ):
        card = Card(
            card_number=card_number,
            batch_number=batch_number,
            batch_date=batch_date,
            batch_name=batch_name,
            batch_position=batch_position
        )
        card_exists = self.get_card_by_card_number(card_number)
        if card_exists:
            raise Exception(f"Error: card with number {card.card_number} already exists")
        with Session(self.engine, expire_on_commit=False) as session:
            session.add(card)
            session.commit()
            return card

    def get_card_by_card_number(self, card_number: int):
        try:
            with Session(self.engine) as session:
                cards = session.scalars(select(Card).where(Card.card_number == card_number))
                if cards:
                    card = cards.one()
                else:
                    return None
            return card
        except Exception as e:
            return None
