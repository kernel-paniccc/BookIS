from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger, ForeignKey
from flask_login import UserMixin

from dotenv import load_dotenv
import os

load_dotenv()

engine = create_async_engine(os.getenv('URL'))
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    books = relationship("Book", back_populates="user")

class Book(Base, UserMixin):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    autor: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    genre: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    user = relationship("User", back_populates="books")


async def async_main():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)