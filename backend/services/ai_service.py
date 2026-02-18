from typing import List
import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

def _safe_parse_json(text: str):
    try:
        t = text.strip()
        if t.startswith("```json"):
            t = t.replace("```json", "").replace("```", "").strip()
        elif t.startswith("```"):
            t = t.replace("```", "").strip()
        return json.loads(t)
    except Exception:
        return None

# ------------------------
# --- Resumo Cultural ---
# ------------------------
def generate_cultural_snapshot(city: str, interests: List[str] = None) -> str:
    interesses = ", ".join(interests) if interests else "geral"
    prompt = f"""
Você é um assistente de inteligência cultural.
Crie um resumo conciso sobre {city} focando nos interesses: {interesses}.
Inclua:
- Ritmo social e horários típicos
- Como os moradores usam a cidade (insights de fóruns)
- Erros comuns de turistas

Escreva em português, de forma amigável, objetiva e com bullet points. Inclua comentários de pessoas do Reddit ou outros fóruns.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text or ""

# --------------------------------
# --- Sugestões Viver a Cidade --- 
# --------------------------------
def generate_live_city_suggestions(
    city: str,
    mood: str,
    budget: str,
    interests: List[str] = None
) -> List[dict]:
    """
    Gera 3 sugestões de experiências para viver a cidade como local,
    considerando mood, budget e interesses.
    Cada item retorna:
    - what_to_do
    - when_to_go
    - vibe
    - cost
    """
    interesses = ", ".join(interests) if interests else "geral"
    prompt = f"""
Você é um assistente de viagens especialista em {city}.
Crie 3 sugestões de experiências para viver a cidade como local, considerando:
- Mood do usuário: {mood}
- Orçamento: {budget}
- Interesses: {interesses}

Cada sugestão deve ter:
- what_to_do (o que fazer)
- when_to_go (melhor horário/dia)
- vibe (tipo de experiência)
- cost (barato, médio, caro)

Retorne SOMENTE um array JSON em português, sem texto extra.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    suggestions = _safe_parse_json(response.text)
    if isinstance(suggestions, list):
        return suggestions
    return [{"info": response.text or ""}]

# ------------------------
# --- Segredos locais ---
# ------------------------
def generate_local_secrets(city: str,
    mood: str,
    budget: str,
    interests: List[str] = None) -> List[dict]:
    """
    Gera 3 segredos locais (nome, por que gostam, melhor horário, custo)
    Retorna sempre lista de dicionários.
    """
    interesses = ", ".join(interests) if interests else "geral"
    prompt = f"""
Você é um guia local expert em {city}.
Crie 3 Segredos Locais que turistas não conhecem, considerando o budget: {budget}, focando no mood do usuário: {mood}, e interesses: {interesses}. Inclua comentários de pessoas do Reddit ou outros fóruns.
Cada item deve ter:
- name (nome do local ou experiência)
- why_locals_like_it (por que os locais gostam)
- best_time (melhor horário/dia)
- cost_level (barato, médio, caro)
Retorne SOMENTE um array JSON, sem texto adicional.
"""
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    secrets = _safe_parse_json(response.text)
    if isinstance(secrets, list):
        return secrets
    return [{"info": response.text or ""}]
