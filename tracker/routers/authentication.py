from fastapi import APIRouter, Depends, HTTPException
from tracker.auth.utils import get_password_hash, verify_password, generate_jwt_for_user
from tracker.models.user import UserIn, UserLogin
from tracker.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from tracker.database import UserTable

router = APIRouter()

@router.post("/register", status_code=201)
async def register_user(user: UserIn, db: AsyncSession = Depends(get_db)):
    # Check if the username or email already exists
    existing_user = await db.execute(
        text("SELECT * FROM users WHERE username = :username"),
        {"username": user.username}
    )
    if existing_user.first():
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create a new user instance using the ORM model
    new_user = UserTable(
        username=user.username,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )

    # Add the user to the database
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token: str = generate_jwt_for_user(user.username)


    return {
        "message": "User registered successfully",
        "access_token": token["access_token"],
        "token_type": token["token_type"],
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "first_name": new_user.first_name,
            "last_name": new_user.last_name
        }
    }

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
        raise HTTPException(status_code=401, detail="Invalid username")

    # Convert the row to a dictionary
    user_dict = dict(db_user._mapping)  # Use _mapping to access row as a dictionary

    if not verify_password(user.password, user_dict["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    # Generate the access token
    token: str = generate_jwt_for_user(user.username)

    return {
        "access_token": token["access_token"],
        "token_type": token["token_type"],
        "user": {
            "id": user_dict["id"],
            "username": user_dict["username"],
            "first_name": user_dict["first_name"],
            "last_name": user_dict["last_name"]
        }
    }