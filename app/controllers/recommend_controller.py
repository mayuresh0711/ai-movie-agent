from app.controllers import user_controller
from app.services import tmdb_service
from app.services import email_service
from app.ai_agent import ask_ai

def generate_recommendation_for_user(user_id: int):
    # Step 1: Get user data and preferences
    user = user_controller.get_user_by_id(user_id)
    if not user or "error" in user:
        return {"error": f"User with ID {user_id} not found."}
    
    user_preferences = user.get("preferences")
    if not user_preferences or "genres" not in user_preferences:
        return {"error": "User preferences or genres not set."}
    
    # Step 2: Get a list of movies based on user's favorite genres
    genre_names = user_preferences["genres"]
    movies = tmdb_service.get_movies_by_genres(genre_names)
    if not movies or "error" in movies:
        return movies # Return the error from the service

    # Step 3: Build a detailed prompt for the AI
    movie_list_str = "\n".join([f"- {m['title']}: {m['overview']}" for m in movies])

    prompt = (
        f"A user named {user['name']} likes the following movie genres: {', '.join(genre_names)}. "
        f"Based on these preferences, please analyze the following list of popular movies and recommend the top 3. "
        f"For each recommendation, provide a short, personalized reason why {user['name']} would enjoy it. "
        f"Make the recommendations sound exciting and engaging.\n\n"
        f"Here is the list of movies to analyze:\n{movie_list_str}"
    )

    # Step 4: Get the AI's recommendation
    ai_recommendation = ask_ai(prompt)

    return {"user": user, "recommendation": ai_recommendation}

def send_recommendation_email(user_id: int):
    # Step 1: Generate the recommendation content
    result = generate_recommendation_for_user(user_id)
    if "error" in result:
        return result

    user = result.get("user")
    recommendation_text = result.get("recommendation")
    user_email = user.get("email")

    if not user_email:
        return {"error": "User does not have an email address."}
    
    # Step 2: Send the email
    subject = f"🎬 Your Personalized Movie Picks, {user.get('name')}!"
    
    email_status = email_service.send_email(
        to_email=user_email,
        subject=subject,
        body=recommendation_text
    )

    return email_status