from fastapi import APIRouter, HTTPException, status, Depends, Header
from sqlalchemy.ext.asyncio import AsyncSession
from tracker.database import get_db
from tracker.routers.utils import get_token, verify_user_id
from tracker.auth.utils import verify_and_refresh_jwt
from jose import JWTError
from tracker.models.application import ApplicationIn

router = APIRouter()

@router.post("/")
async def create_application(application: ApplicationIn,
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

    await verify_user_id(db, application.user_id, username)
    

    print(f"Creating application for user {username} with data: {application}")

    return {
        "message": "Application created successfully",
        "application": application
    }


    
    