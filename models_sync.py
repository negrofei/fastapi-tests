from enum import Enum
from typing import List

from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Numeric
from sqlalchemy.orm import (  # Cosas de conexiones con la base de datos
    Session, declarative_base
)

# import getpass
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def start_your_engine() -> Engine:
    """
    Armamos el objeto engine que se comunica con la base de datos
    """
    engine = create_engine(
        'mysql+pymysql://{user}:{pwd}@{host}:3306/{db}'.format(
            user='root', 
            # pwd=getpass.getpass('Password: '),
            pwd='JRR-ElUltimo10',
            host='localhost',
            db='fastapi'
        )
    )
    

    return engine

engine = start_your_engine()
Base = declarative_base()
Base.metadata.create_all(engine)

# @contextlib.contextmanager
def get_session():
    session = Session(bind=engine)
    Base.metadata.create_all(engine)

    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()


### Models for API
class Category(Enum):
    """Category of an item"""
    tools = 'tools'
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
    name: str = Field(description="Name of the item")
    price: float = Field(description="Price of the item")
    quantity: int = Field(description="Amount of instances of this item in stock")
    category: Category = Field(description="Category")

### Models for SQL 
class DBItem(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40))
    price = Column(Numeric(7,4))
    quantity = Column(Integer)
    category = Column(String(40))
    def __repr__(self):
        return f"<DBItem(id={self.id!r}, name={self.name!r})"  




