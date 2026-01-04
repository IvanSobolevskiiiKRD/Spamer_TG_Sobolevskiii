from sqlalchemy import BigInteger, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    username: Mapped[str] = mapped_column()
    admin: Mapped[bool] = mapped_column()

class Account(Base):
    __tablename__ = "acconts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    api_id: Mapped[str] = mapped_column()
    api_hash: Mapped[str] = mapped_column()
    phone_number: Mapped[str] = mapped_column()
    activated: Mapped[bool] = mapped_column()

class Group(Base):
    __tablename__ = "Groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column()
    count_minuts: Mapped[int] = mapped_column()
    message: Mapped[str] = mapped_column()
    next_message: Mapped[DateTime] = mapped_column(DateTime)
    work_type: Mapped[bool] = mapped_column()


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)