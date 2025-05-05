from fastapi import APIRouter, Depends, HTTPException
from tracker.auth.utils import get_password_hash, verify_password, create_access_token
from tracker.models.user import UserIn, UserLogin
from tracker.database import async_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from tracker.database import UserTable  # Import the User table model
from datetime import timedelta


ACCESS_TOKEN_EXPIRE_MINUTES = 60

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
    hashed_password = get_password_hash(user.password)

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

@router.post("/login")
async def login_user(user: UserLogin, db: AsyncSession = Depends(get_db)):
    # Fetch the user from the database
    result = await db.execute(
        text("SELECT * FROM users WHERE username = :username"),
        {"username": user.username}
    )
    db_user = result.fetchone()  # Fetch the first row

    # Check if the user exists and verify the password
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Convert the row to a dictionary
    user_dict = dict(db_user._mapping)  # Use _mapping to access row as a dictionary

    if not verify_password(user.password, user_dict["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate the access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user_dict["username"]}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}