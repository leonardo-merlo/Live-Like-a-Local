# backend/test_ai.py
from services.ai_service import generate_cultural_snapshot, generate_local_secrets
import json

# Texto de teste para Cultural Snapshot
texto_cultural = """
Posts sobre cultura brasileira, hábitos locais, festas populares e lugares turísticos.
Inclui comentários de moradores sobre restaurantes, transporte e eventos da cidade.
"""

# Texto de teste para Local Secrets
texto_secrets = """
Dados sobre pontos de interesse locais, dicas de moradores, restaurantes e experiências culturais únicas.
"""

# --- Teste Cultural Snapshot ---
print("=== Cultural Snapshot ===")
resultado_cultural = generate_cultural_snapshot(texto_cultural)
print(resultado_cultural)
print("\n")

# --- Teste Local Secrets ---
print("=== Local Secrets ===")
resultado_secrets = generate_local_secrets(texto_secrets)

# Se for lista de dicts, printa bonito em JSON
print(json.dumps(resultado_secrets, indent=2, ensure_ascii=False))
