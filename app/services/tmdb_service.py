import os
import requests
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
TMDB_API_URL = "https://api.themoviedb.org/3/discover/movie"

# TMDb uses numeric IDs for genres. This dict maps names to IDs.
GENRE_MAP = {
    "Action": 28,
    "Comedy": 35,
    "Drama": 18,
    "Science Fiction": 878,
    "Fantasy": 14,
    "Horror": 27,
    "Romance": 10749,
    "Thriller": 53
}

def get_movies_by_genres(genre_names: list[str]) -> list[dict]:
    """
    Fetches a list of popular movies from TMDb based on genre names.
    """
    if not TMDB_API_KEY:
        return {"error": "TMDb API key not found"}

    # Convert genre names to a comma-separated string of genre IDs
    genre_ids = [str(GENRE_MAP.get(name)) for name in genre_names if name in GENRE_MAP]
    if not genre_ids:
        return {"error": "Invalid or no genres provided"}
    
    genre_id_string = ",".join(genre_ids)

    params = {
        "api_key": TMDB_API_KEY,
        "sort_by": "popularity.desc",
        "with_genres": genre_id_string,
        "language": "en-US",
        "page": 1
    }

    try:
        response = requests.get(TMDB_API_URL, params=params)
        response.raise_for_status()  # Raises an exception for bad status codes
        
        # We only need a few details for each movie
        movies_data = response.json().get('results', [])
        movies = [
            {
                "title": movie.get("title"),
                "overview": movie.get("overview")
            }
            for movie in movies_data[:10] # Get top 10 popular movies
        ]
        return movies

    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}