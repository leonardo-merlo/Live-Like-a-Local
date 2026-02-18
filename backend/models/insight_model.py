from pydantic import BaseModel
from typing import List

class LocalSecret(BaseModel):
    name: str
    why_locals_like_it: str
    best_time: str
    cost_level: str

class Suggestion(BaseModel):
    what_to_do: str
    when_to_go: str
    vibe: str
    cost: str

class InsightResponse(BaseModel):
    cultural_snapshot: str
    local_secrets: List[LocalSecret]
    suggestions: List[Suggestion]
