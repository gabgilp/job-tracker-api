from fastapi import APIRouter, HTTPException, status, Depends, Header
from tracker.auth.utils import verify_and_refresh_jwt
from tracker.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError
from tracker.models.user import UserResponse
from tracker.routers.utils import get_token, get_user_from_db

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

    user = await get_user_from_db(db, username)
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


    