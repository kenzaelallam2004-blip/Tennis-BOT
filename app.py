import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
import random
from gtts import gTTS

# ============================================================
# CONFIG
# ============================================================
st.set_page_config(page_title="🎾 Tennis BOT", layout="wide")

# ============================================================
# CSS + BACKGROUND + ANIMATION BALLS
# ============================================================
st.markdown("""
<style>

/* ================= BACKGROUND ================= */
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

/* ================= FLOATING BALLS ================= */
.ball {
    position: fixed;
    width: 10px;
    height: 10px;
    background: #f1c40f;
    border-radius: 50%;
    box-shadow: 0 0 10px rgba(255,255,255,0.4);
    animation: floatBall 8s linear infinite;
    z-index: 0;
    opacity: 0.7;
}

@keyframes floatBall {
    0% {
        transform: translateY(100vh) scale(0.5);
        opacity: 0;
    }
    20% {
        opacity: 1;
    }
    100% {
        transform: translateY(-10vh) scale(1);
        opacity: 0;
    }
}

.ball:nth-child(1) { left: 10%; animation-delay: 0s; }
.ball:nth-child(2) { left: 25%; animation-delay: 2s; }
.ball:nth-child(3) { left: 40%; animation-delay: 4s; }
.ball:nth-child(4) { left: 60%; animation-delay: 1s; }
.ball:nth-child(5) { left: 80%; animation-delay: 3s; }
.ball:nth-child(6) { left: 90%; animation-delay: 5s; }

/* ================= UI ================= */
.center-btn {
    display: flex;
    justify-content: center;
}

</style>

<!-- 🎾 Floating balls -->
<div class="ball"></div>
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
# RESET
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
        "Débutant": "Travaille ton timing.",
        "Intermédiaire": "Bon rythme, améliore ton placement.",
        "Avancé": "Excellent contrôle, varie les trajectoires."
    }

    msg = base[level]

    if precision > 6:
        msg += " Trop d'écart."
    if speed > 120:
        msg += " Trop de puissance."

    return msg

# ============================================================
# VOIX (SAFE CLOUD)
# ============================================================
def speak(text):
    try:
        tts = gTTS(text=text, lang="fr")
        tts.save("coach.mp3")
        st.audio("coach.mp3")
    except:
        st.warning("Audio indisponible")

# ============================================================
# PAGE 1 - HOME
# ============================================================
if st.session_state.step == 0:

    col1, col2 = st.columns(2)

    with col1:
        if os.path.exists("machine.jpg"):
            st.image("machine.jpg", width=350)

    with col2:
        st.title("🎾 Tennis BOT")
        st.write("""
        Machine intelligente :
        - vitesse
        - effet
        - précision
        """)

    st.markdown('<div class="center-btn">', unsafe_allow_html=True)

    if st.button("🚀 Démarrer"):
        st.session_state.step = 1
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# PAGE 2 - PROFILE
# ============================================================
elif st.session_state.step == 1:

    st.title("📝 Profil joueur")

    with st.form("form"):

        nom = st.text_input("Nom")
        age = st.text_input("Âge")

        frequence = st.selectbox(
            "Fréquence",
            ["1/semaine", "2/semaine", "3-4/semaine", "Tous les jours"]
        )

        anciennete = st.selectbox(
            "Ancienneté",
            ["<1 an", "1 an", "2 ans", "3-5 ans", "5+ ans"]
        )

        niveau = st.selectbox("Niveau", ["Débutant", "Intermédiaire", "Avancé"])

        ok = st.form_submit_button("Valider")

        if ok and nom:

            base_speed = {"Débutant": 60, "Intermédiaire": 85, "Avancé": 110}[niveau]

            st.session_state.user = {
                "Nom": nom,
                "Âge": age,
                "Niveau": niveau,
                "base_speed": base_speed
            }

            st.session_state.step = 2
            st.rerun()

# ============================================================
# PAGE 3 - TRAINING + 3D
# ============================================================
elif st.session_state.step == 2:

    u = st.session_state.user

    st.success(f"Bienvenue {u['Nom']} 🎾")

    speed = st.slider("Vitesse", 30, 150, u["base_speed"])
    spin = st.slider("Effet", 0, 15, 5)

    if st.button("Lancer 🎾"):

        x = np.random.normal(0, 3.5)
        precision = abs(x) * 2

        st.session_state.history.append({
            "Speed": speed,
            "Spin": spin,
            "Precision": precision,
            "Zone": "OK" if precision < 6 else "MISS"
        })

        msg = coach(speed, spin, precision, u["Niveau"])

        st.subheader("🤖 Coach IA")
        st.info(msg)

        speak(msg)

        # ====================================================
        # 🎾 3D SIMULATION
        # ====================================================
        t = np.linspace(0, 1, 30)

        x_traj = np.zeros_like(t)
        y_traj = 10 * t
        z_traj = 4 * t * (1 - t) * speed / 90

        fig = go.Figure()

        fig.add_trace(go.Scatter3d(
            x=x_traj,
            y=y_traj,
            z=z_traj,
            mode="lines+markers",
            line=dict(color="yellow", width=6),
            name="Ball"
        ))

        fig.add_trace(go.Scatter3d(
            x=[0],
            y=[10],
            z=[0],
            mode="markers",
            marker=dict(size=8, color="red"),
            name="Impact"
        ))

        st.plotly_chart(fig, use_container_width=True)

    # ============================================================
    # HISTORIQUE
    # ============================================================
    if len(st.session_state.history) > 0:

        df = pd.DataFrame(st.session_state.history)

        st.markdown("## 📊 Historique")

        st.dataframe(df)

        st.metric("Total tirs", len(df))
        st.metric("Precision moyenne", round(df["Precision"].mean(), 2))
        st.metric("Taux réussite", f"{(df['Zone']=='OK').mean()*100:.1f}%")

    if st.button("🔄 Restart"):
        reset_all()
