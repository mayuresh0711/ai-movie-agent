from fastapi import APIRouter
from app.models import UserCreate
from app.controllers import user_controller

router = APIRouter()

@router.post("/users", tags=["Users"])
def signup_user(user: UserCreate):
    """
    Endpoint to create a new user.
    Receives user name, email, and preferences and saves them to the DB.
    """
    return user_controller.create_new_user(user)