from enum import Enum
from typing import List

from pydantic import BaseModel, Field, constr, confloat, conint
from sqlalchemy.orm import (  # Cosas de conexiones con la base de datos
    DeclarativeBase,
    Mapped,
    mapped_column,
)

from sqlalchemy.engine import Engine

# ASYNC
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


def start_your_engine() -> Engine:
    """
    Armamos el objeto engine que se comunica con la base de datos
    """
    engine = create_async_engine(
        "mysql+aiomysql://{user}:{pwd}@{host}:3306/{db}".format(
            user="root",
            # pwd=getpass.getpass('Password: '),
            pwd="JRR-ElUltimo10",
            host="localhost",
            db="fastapi",
        ),
        echo=True,
    )

    return engine


engine = start_your_engine()


async def get_session():
    # session = Session(bind=engine)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session = AsyncSession(engine)

    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        await session.close()


### Models for API
class Category(Enum):
    """Category of an item"""

    tools = "tools"
    consumables = "consumables"

    @classmethod
    def __get_validators__(cls) -> List:
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not isinstance(value, cls):
            if isinstance(value, str):
                try:
                    cls[value]
                    return value
                except KeyError:
                    pass
            raise ValueError(f"Invalid enumeration member: {value}")
        return value


class Item(BaseModel):
    """Representation of an item in the system."""

    # id: int = Field(description="Unique integer that specifies this item.")
    name: constr(min_length=1, max_length=25) = Field(description="Name of the item")
    price: confloat(ge=0) = Field(description="Price of the item")
    quantity: conint(ge=0) = Field(
        description="Amount of instances of this item in stock"
    )
    category: Category = Field(description="Category")


### Models for SQL
class Base(DeclarativeBase):
    pass


class DBItem(Base):
    __tablename__ = "items"
    # id = Column(Integer, primary_key=True, autoincrement=True)
    id: Mapped[int] = mapped_column(primary_key=True)
    # name = Column(String(40))
    name: Mapped[str] = mapped_column(unique=True)
    # price = Column(Numeric(7,4))
    price: Mapped[float] = mapped_column()
    # quantity = Column(Integer)
    quantity: Mapped[int] = mapped_column()
    # category = Column(String(40))
    category: Mapped[Category] = mapped_column()

    def __repr__(self):
        return f"<DBItem(id={self.id!r}, name={self.name!r})"
