from pydantic import BaseModel
from typing import List

class InsightRequest(BaseModel):
    city: str
    mood: str
    interests: List[str]
    budget: str
