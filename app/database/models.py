from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy import BigInteger
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

async def async_main():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.create_all)