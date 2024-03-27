from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    telegram_id = Column(
        BigInteger,
        unique=True,
        nullable=False,
        primary_key=True
    )
    tasks = relationship('Task', backref='user')


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    todo = Column(String(200), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.telegram_id'))
    completed = Column(Boolean, default=False)

    def __str__(self):
        return self.todo


engine = create_async_engine(
    'postgresql+asyncpg://postgres:12345@localhost:5432/aogram',
    echo=True
)
async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
    )
