from fastapi import APIRouter
from app.controllers import recommend_controller

router = APIRouter()

@router.get("/recommendations/{user_id}", tags=["Recommendations"])
def get_recommendation(user_id: int):
    """
    Generates personalized movie recommendations for a given user ID.
    """
    return recommend_controller.generate_recommendation_for_user(user_id)


@router.post("/recommendations/{user_id}/send-email", tags=["Recommendations"])
def send_recommendation(user_id: int):
    """
    Generates and sends personalized movie recommendations to the user's email.
    """
    return recommend_controller.send_recommendation_email(user_id)