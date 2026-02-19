import streamlit as st
import requests
import os
from dotenv import load_dotenv


load_dotenv()
access_key = os.getenv("UNSPLASH_ACCESS_KEY")

st.set_page_config(page_title="Live Like a Local", page_icon="🌎", layout="wide")
st.title("Live Like a Local — IA para Viagens")


# --- Inputs ---
st.header("Informe seus dados")
city = st.text_input("Destino", "São Paulo")
mood = st.selectbox("Vibe", ["Relaxar", "Explorar", "Socializar", "Energizar"])
interests = st.multiselect(
    "Interesses (máx 2)",
    ["Comida", "Cultura", "Natureza", "Vida noturna", "Movimento / Esportes", "Música"],
    default=[]
)
if len(interests) > 2:
    st.warning("Escolha no máximo 2 interesses")
    interests = interests[:2]
budget = st.selectbox("Orçamento", ["Baixo", "Médio", "Alto"])

# --- Botão ---
if st.button("Gerar Insights"):
    with st.spinner("Gerando insights, aguarde..."):
        payload = {
            "city": city,
            "mood": mood,
            "interests": interests,
            "budget": budget
        }
        try:
            response = requests.post("https://live-like-a-local.onrender.com/generate-insight", json=payload)
            if response.status_code == 200:
                data = response.json()

                # --- Imagem ---
                url = f"https://api.unsplash.com/search/photos?query={city}&client_id={access_key}&per_page=1"
                res = requests.get(url).json()

                city_image_url = None

                if "results" in res and len(res["results"]) > 0:
                    city_image_url = res["results"][0]["urls"]["regular"]

                if city_image_url:
                    st.markdown(f"""
                    <div style="width: 100%;
                    max-height: 420px;
                    overflow: hidden;
                    border-radius: 16px;
                    display: flex;
                    justify-content: center;
                    align-items: center;">
                        <img src="{city_image_url}" style="width: 100%; height: 100%; object-fit: contain;">
                    </div>
                    <p style="text-align:center; font-size:14px; color:gray;">
                    Explorando {city}
                    </p>
                    """, unsafe_allow_html=True)
                else:
                    st.info("Imagem não encontrada para essa cidade.")


                # --- Resumo Cultural ---
                st.subheader("🗺️ Resumo Cultural")
                st.write(data.get("cultural_snapshot", "Nenhum dado"))

                # --- Sugestões Viver a Cidade ---
                st.subheader("💡 Sugestões para Viver a Cidade")

                for sug in data.get("suggestions", []):
                    st.markdown(f"""
                **{sug.get('what_to_do', '')}**  
                Quando: {sug.get('when_to_go', '')}  
                Vibe: {sug.get('vibe', '')}  
                Custo: {sug.get('cost', '')}
                """)
                    st.markdown("")  

                # --- Segredos locais ---
                st.subheader("🔒 Segredos Locais")

                for secret in data.get("local_secrets", []):
                    st.markdown(f"""
                **{secret.get('name', '')}**  
                Por que os locais gostam: {secret.get('why_locals_like_it', '')}  
                Melhor horário: {secret.get('best_time', '')}  
                Nível de custo: {secret.get('cost_level', '')}
                """)
                    st.markdown("") 


            else:
                st.error(f"Erro ao chamar backend: {response.status_code}")
        except Exception as e:
            st.error(f"Erro de conexão: {e}")
