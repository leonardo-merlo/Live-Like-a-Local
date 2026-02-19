# backend/services/recommendation_service.py

from typing import List, Dict
import random

# ------------------------
# Mapeamento mood → categorias
# ------------------------
MOOD_TO_CATEGORIES = {
    "Relaxar": ["nature", "coffee", "spa", "relax"],
    "Explorar": ["culture", "history", "urban", "arquitecture", "museums"],
    "Socializar": ["nightlife", "food", "bars", "party", "events", "music"],
    "Energizar": ["movement", "sports", "adventure"]
}

def map_mood_to_categories(mood: str) -> List[str]:
    """Retorna categorias de lugares com base no mood do usuário."""
    return MOOD_TO_CATEGORIES.get(mood, [])

# ------------------------
# Mapeamento budget → nível de custo
# ------------------------
BUDGET_TO_LEVEL = {
    "Baixo": "Barato",
    "Médio": "Médio",
    "Alto": "Caro"
}

def filter_by_budget(places: List[Dict], budget: str) -> List[Dict]:
    """Filtra lugares pelo nível de custo baseado no budget do usuário."""
    level = BUDGET_TO_LEVEL.get(budget)
    if not level:
        return places
    return [p for p in places if p.get("cost_level") == level]

# ------------------------
# Seleção de Local Secrets
# ------------------------
def select_local_secrets(places: List[Dict]) -> List[Dict]:
    """
    Seleciona 3 itens: 1 food, 1 vibe, 1 wildcard.
    Se algum não existir, pega o primeiro disponível.
    """
    secrets = {"food": None, "vibe": None, "wildcard": None}

    for p in places:
        category = p.get("category", "").lower()
        if category == "food" and not secrets["food"]:
            secrets["food"] = p
        elif category == "vibe" and not secrets["vibe"]:
            secrets["vibe"] = p
        elif category not in ["food", "vibe"] and not secrets["wildcard"]:
            secrets["wildcard"] = p

    # fallback: se algum estiver vazio, pega aleatório
    for key in secrets:
        if not secrets[key] and places:
            secrets[key] = random.choice(places)

    return list(secrets.values())

# ------------------------
# Sugestões Live This City
# ------------------------
# filtro corrigido: verifica se a categoria do lugar contém alguma categoria mapeada
def select_places_for_suggestions(places: list, categories: list) -> list:
    """Filtra lugares cujas categorias contenham pelo menos uma das categorias do mood."""
    filtered = []
    for p in places:
        place_cats = p.get("category", "").lower().split(",") 
        if any(cat.lower() in place_cats for cat in categories):
            filtered.append(p)
    return filtered


def generate_live_suggestions(places: List[dict]) -> List[dict]:
    if not places:
        return []
    return random.sample(places, min(3, len(places)))

