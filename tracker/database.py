from databases import Database
from tracker.config import config
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

DB_URL = config.DB_URL

database = Database(DB_URL)

engine = create_async_engine(DB_URL)

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    applications = relationship("ApplicationTable", back_populates="user")

class ApplicationTable(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,  ForeignKey("users.id"), index=True, nullable=False)
    company_name = Column(String, index=True, nullable=False)
    position_title = Column(String, index=True, nullable=False)
    status = Column(String, index=True, nullable=False)
    notes = Column(Text)
    date_applied = Column(String, index=True, nullable=False)
    posting_url = Column(Text, index=True)

    user = relationship("UserTable", back_populates="applications")


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)