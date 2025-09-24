from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any

class UserCreate(BaseModel):
    name: str
    email: EmailStr  # This validates the email format automatically
    preferences: Dict[str, Any] # e.g., {"genres": ["Action", "Sci-Fi"]}