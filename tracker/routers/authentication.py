from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from tracker.models.user import User, UserIn
from tracker.database import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from tracker.database import UserTable  # Import the User table model

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

async def get_db():
    async with async_session() as session:
        yield session

@router.post("/register", status_code=201)
async def register_user(user: UserIn, db: AsyncSession = Depends(get_db)):
    # Check if the username or email already exists
    existing_user = await db.execute(
        text("SELECT * FROM users WHERE username = :username OR email = :email"),
        {"username": user.username, "email": user.email}
    )
    if existing_user.first():
        raise HTTPException(status_code=400, detail="Username or email already registered")

    # Hash the password
    hashed_password = pwd_context.hash(user.password)

    # Create a new user instance using the ORM model
    new_user = UserTable(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )

    # Add the user to the database
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "User registered successfully"}