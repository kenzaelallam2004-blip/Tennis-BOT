import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
import random
from gtts import gTTS

# ============================================================
# CONFIG PAGE
# ============================================================
st.set_page_config(page_title="🎾 Tennis BOT ", layout="wide")

# ============================================================
# CSS + BACKGROUND + BALLS
# ============================================================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(-45deg, #0b3d2e, #145a32, #1f7a4a, #58d68d);
    background-size: 400% 400%;
    animation: gradientBG 10s ease infinite;
}

@keyframes gradientBG {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 🎾 floating balls */
.ball {
    position: fixed;
    width: 14px;
    height: 14px;
    background: #f1c40f;
    border-radius: 50%;
    animation: float 8s linear infinite;
    z-index: 0;
}

@keyframes float {
    0% { transform: translateY(100vh); opacity: 0; }
    50% { opacity: 1; }
    100% { transform: translateY(-10vh); opacity: 0; }
}

.ball:nth-child(1){left:10%;}
.ball:nth-child(2){left:25%; animation-delay:2s;}
.ball:nth-child(3){left:40%; animation-delay:4s;}
.ball:nth-child(4){left:60%; animation-delay:1s;}
.ball:nth-child(5){left:80%; animation-delay:3s;}

.glass {
    background: rgba(255,255,255,0.75);
    padding: 20px;
    border-radius: 20px;
}

/* bouton centré */
.center-btn {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

</style>

<div class="ball"></div>
<div class="ball"></div>
<div class="ball"></div>
<div class="ball"></div>
<div class="ball"></div>

""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================
if "step" not in st.session_state:
    st.session_state.step = 0

if "user" not in st.session_state:
    st.session_state.user = {}

if "history" not in st.session_state:
    st.session_state.history = []

# ============================================================
# RESET / QUIT
# ============================================================
def reset_all():
    st.session_state.step = 0
    st.session_state.user = {}
    st.session_state.history = []
    st.rerun()

# ============================================================
# COACH IA
# ============================================================
def coach(speed, spin, precision, level):

    base = {
        "Débutant": ["Travaille ton timing.", "Sois plus stable."],
        "Intermédiaire": ["Bon rythme, ajuste ton placement."],
        "Avancé": ["Excellent niveau, varie tes trajectoires."]
    }

    msg = random.choice(base[level])

    if precision > 6:
        msg += " Trop d'écart."
    if speed > 120:
        msg += " Trop puissant."

    return msg

# ============================================================
# VOIX
# ============================================================
def speak(text):
    tts = gTTS(text=text, lang="fr")
    tts.save("coach.mp3")
    st.audio("coach.mp3")

# ============================================================
# PAGE 1 - ACCUEIL
# ============================================================
if st.session_state.step == 0:

    col1, col2 = st.columns(2)

    with col1:
        if os.path.exists("machine.jpg"):
            st.image("machine.jpg", width=350)

    with col2:
        st.title("🎾 Tennis BOT")

        st.write("""
        Machine intelligente d'entraînement qui adapte automatiquement :
        - ⚡ vitesse
        - 🌀 effet
        - 🎯 précision
        
        Entraîne-toi comme un joueur professionnel.
        Commence ton propre entrainement avec nous!
        """)

    st.markdown('<div class="center-btn">', unsafe_allow_html=True)

    if st.button("🚀 Démarrer l'expérience"):
        st.session_state.step = 1
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE 2 - FORMULAIRE
# ============================================================
elif st.session_state.step == 1:

    st.title("📝 Profil joueur")

    with st.form("form"):

        nom = st.text_input("Nom")

        # âge clavier
        age = st.text_input("Âge")

        frequence = st.selectbox(
            "Fréquence de jeu",
            ["1 fois/semaine", "2 fois/semaine", "3-4 fois/semaine", "Tous les jours"]
        )

        anciennete = st.selectbox(
            "Ancienneté (années de pratique)",
            ["<1 an", "1 an", "2 ans", "3-5 ans", "5+ ans"]
        )

        niveau = st.selectbox("Niveau", ["Débutant", "Intermédiaire", "Avancé"])

        ok = st.form_submit_button("Valider")

        if ok and nom:

            base_speed = {"Débutant": 60, "Intermédiaire": 85, "Avancé": 110}[niveau]

            st.session_state.user = {
                "Nom": nom,
                "Âge": age,
                "Fréquence": frequence,
                "Ancienneté": anciennete,
                "Niveau": niveau,
                "base_speed": base_speed
            }

            st.session_state.step = 2
            st.rerun()

# ============================================================
# PAGE 3 - SIMULATION
# ============================================================
elif st.session_state.step == 2:

    u = st.session_state.user

    st.success(f"Bienvenue {u['Nom']} 🎾")

    speed = st.slider("Vitesse", 30, 150, u["base_speed"])
    spin = st.slider("Effet", 0, 15, 5)

    if st.button("Lancer la balle 🎾"):

        x = np.random.normal(0, 4)
        precision = abs(x) * 2

        st.session_state.history.append({
            "Speed": speed,
            "Precision": precision,
            "Zone": "OK" if precision < 6 else "MISS"
        })

        msg = coach(speed, spin, precision, u["Niveau"])

        st.markdown("### 🤖 Coach IA")
        st.info(msg)

        speak(msg)

        fig = go.Figure()
        fig.add_trace(go.Scatter3d(
            x=[0,0,0],
            y=[0,10,12],
            z=[0,0,1],
            mode="lines"
        ))

        st.plotly_chart(fig)

    st.markdown("---")

    if st.button("📊 Voir l'historique"):
        st.session_state.step = 3
        st.rerun()

# ============================================================
# PAGE 4 - HISTORIQUE
# ============================================================
elif st.session_state.step == 3:

    st.title("📊 Historique joueur")

    if st.session_state.history:

        df = pd.DataFrame(st.session_state.history)

        st.dataframe(df)

        st.metric("Total tirs", len(df))
        st.metric("Précision moyenne", round(df["Precision"].mean(), 2))
        st.metric("Taux réussite", f"{(df['Zone']=='OK').mean()*100:.1f}%")

    else:
        st.info("Aucun tir enregistré.")

    st.markdown("---")

    if st.button("⬅ Retour au jeu"):
        st.session_state.step = 2
        st.rerun()

    if st.button("🔄 Nouveau joueur"):
        reset_all()

    # ============================================================
# FOOTER
# ============================================================
st.markdown("""
    <div style="text-align:center; margin-top:40px; padding:20px; 
                color:white; opacity:0.7; font-size:14px;">
        Créé par Nouhaila Bahi et Zainab Edrif 🎾
    </div>
""", unsafe_allow_html=True)    
