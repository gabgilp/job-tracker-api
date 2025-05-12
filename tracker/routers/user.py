from fastapi import APIRouter, HTTPException, status, Depends, Header
from tracker.auth.utils import verify_and_refresh_jwt, generate_jwt_for_user
from tracker.database import get_db, UserTable, ApplicationTable
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from tracker.models.user import UserResponse, UserToModify
from tracker.routers.utils import get_token
from sqlalchemy import select

router = APIRouter()

@router.get("/", response_model=UserResponse)
async def get_user_data(Authorization: str = Header(..., description="Bearer token for authentication"), 
                        db: AsyncSession = Depends(get_db)):
    token = get_token(Authorization)

    try:
        decoded_token = verify_and_refresh_jwt(token)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=str(e))
    
    username = decoded_token["username"]

    user = await db.execute(
        select(UserTable).where(UserTable.username == username)
    )
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="User not found")
    
    return {
        "user" : {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "id": user.id
        },
        "new_token": decoded_token["new_token"],
        "token_type": "bearer"
    }

@router.put("/", response_model=UserResponse)
async def update_user_data(updated_user: UserToModify,
                           Authorization: str = Header(..., description="Bearer token for authentication"), 
                            db: AsyncSession = Depends(get_db)):
    token = get_token(Authorization)

    try:
        decoded_token = verify_and_refresh_jwt(token)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=str(e))
    
    username = decoded_token["username"]

    user = await db.execute(
        select(UserTable).where(UserTable.username == username)
    )
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    
    if updated_user.username != user.username:
        existing_user = await db.execute(
            select(UserTable).where(UserTable.username == updated_user.username)
        )
        existing_user = existing_user.scalar_one_or_none()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                                detail="Username already taken")
        new_token = generate_jwt_for_user(updated_user.username)["access_token"]
        decoded_token["new_token"] = new_token
    
    user.username = updated_user.username
    user.first_name = updated_user.first_name
    user.last_name = updated_user.last_name
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return {
        "user" : {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "id": user.id
        },
        "new_token": decoded_token["new_token"],
        "token_type": "bearer"
    }
    

@router.delete("/")
async def delete_user(Authorization: str = Header(..., description="Bearer token for authentication"), 
                       db: AsyncSession = Depends(get_db)):
    token = get_token(Authorization)

    try:
        decoded_token = verify_and_refresh_jwt(token)
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail=str(e))
    
    username = decoded_token["username"]

    user = await db.execute(
        select(UserTable).where(UserTable.username == username)
    )
    user = user.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    
    try:
        applications = await db.execute(
            select(ApplicationTable).where(ApplicationTable.user_id == user.id)
        )
        applications = applications.scalars().all()
        for application in applications:
            await db.delete(application)
        await db.delete(user)
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"Error deleting user and associated applications: {str(e)}")

    return {
        "message": "User deleted successfully"
    }