from fastapi import APIRouter
from models.insight_model import InsightResponse, LocalSecret, Suggestion
from models.insight_input import InsightRequest
from services.ai_service import (
    generate_cultural_snapshot,
    generate_local_secrets,
    generate_live_city_suggestions
)

router = APIRouter()

@router.post("/generate-insight", response_model=InsightResponse)
def generate_insight(request: InsightRequest):
    city = request.city
    mood = request.mood
    interests = request.interests
    budget = request.budget

    # --- Resumo Cultural ---
    cultural_snapshot = generate_cultural_snapshot(city, interests)

    # --- Sugestões para Viver a Cidade ---
    suggestions_raw = generate_live_city_suggestions(city, mood, budget, interests)
    suggestions = [
        Suggestion(
            what_to_do=p.get("what_to_do", ""),
            when_to_go=p.get("when_to_go", ""),
            vibe=p.get("vibe", ""),
            cost=p.get("cost", "")
        )
        for p in suggestions_raw
    ]

        # --- Segredos locais ---
    local_secrets_raw = generate_local_secrets(city, mood, budget, interests)
    local_secrets = [
        LocalSecret(
            name=p.get("name", ""),
            why_locals_like_it=p.get("why_locals_like_it", ""),
            best_time=p.get("best_time", ""),
            cost_level=p.get("cost_level", "")
        )
        for p in local_secrets_raw
    ]

    return InsightResponse(
        cultural_snapshot=cultural_snapshot,
        local_secrets=local_secrets,
        suggestions=suggestions
    )
