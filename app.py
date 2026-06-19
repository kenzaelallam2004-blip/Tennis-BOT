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
st.set_page_config(
    page_title="🎾 Tennis BOT",
    layout="wide"
)

# ============================================================
# CSS GLOBAL
# ============================================================
st.markdown("""
<style>
.stButton > button {
    background-color: green !important;
}
.stApp {
    background: linear-gradient(-45deg,
    #0b3d2e,
    #145a32,
    #1f7a4a,
    #58d68d);
    background-size: 400% 400%;
    animation: gradientBG 12s ease infinite;
}

/* Texte blanc partout */
h1,h2,h3,h4,h5,h6,p,label,span {
    color:white !important;
}

[data-testid="stMarkdownContainer"] {
    color:white;
}

@keyframes gradientBG {
    0% {background-position:0% 50%;}
    50% {background-position:100% 50%;}
    100% {background-position:0% 50%;}
}

/* =====================================================
BALLS ANIMATION
===================================================== */

.ball{
position:fixed;
width:16px;
height:16px;
background:#f1c40f;
border-radius:50%;
z-index:0;
animation:floatBall 12s linear infinite;
box-shadow:0 0 10px rgba(255,255,255,0.6);
}

@keyframes floatBall{
0%{
transform:translateY(100vh);
opacity:0;
}
20%{
opacity:1;
}
100%{
transform:translateY(-10vh);
opacity:0;
}
}

.ball:nth-child(1){left:5%;animation-delay:0s;}
.ball:nth-child(2){left:15%;animation-delay:2s;}
.ball:nth-child(3){left:25%;animation-delay:4s;}
.ball:nth-child(4){left:35%;animation-delay:6s;}
.ball:nth-child(5){left:45%;animation-delay:1s;}
.ball:nth-child(6){left:55%;animation-delay:3s;}
.ball:nth-child(7){left:65%;animation-delay:5s;}
.ball:nth-child(8){left:75%;animation-delay:7s;}
.ball:nth-child(9){left:85%;animation-delay:2s;}
.ball:nth-child(10){left:95%;animation-delay:4s;}

/* =====================================================
CARDS
===================================================== */

.glass{
background:rgba(255,255,255,0.12);
backdrop-filter:blur(10px);
padding:25px;
border-radius:20px;
border:1px solid rgba(255,255,255,0.2);
}

.center-btn{
display:flex;
justify-content:center;
margin-top:25px;
}

/* Inputs */
.stTextInput input{
background:white !important;
color:black !important;
}

.stSelectbox div[data-baseweb="select"]{
color:black !important;
}

/* =====================================================
BUTTON TEXT COLOR FIX (AJOUT UNIQUEMENT ICI)
===================================================== */
.stButton > button {
    color: black !important;
    font-weight: 600;
}

/* Footer */
.footer{
text-align:center;
padding:20px;
font-size:15px;
font-weight:bold;
color:white;
opacity:0.85;
}

</style>

<div class="ball"></div>
<div class="ball"></div>
<div class="ball"></div>
<div class="ball"></div>
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
# RESET APP
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

    messages = {
        "Débutant":[
            "Travaille davantage ton timing.",
            "Reste stable sur tes appuis.",
            "Garde les yeux sur la balle."
        ],

        "Intermédiaire":[
            "Très bon rythme.",
            "Ton placement devient intéressant.",
            "Essaie d'accélérer progressivement."
        ],

        "Avancé":[
            "Excellent niveau technique.",
            "Varie davantage les trajectoires.",
            "Très bonne maîtrise de la vitesse."
        ]
    }

    msg = random.choice(messages[level])

    if precision > 6:
        msg += " La précision doit être améliorée."

    if speed > 120:
        msg += " Attention à ne pas sacrifier le contrôle."

    return msg

# ============================================================
# VOIX IA
# ============================================================
def speak(text):
    try:
        tts = gTTS(text=text, lang="fr")
        tts.save("coach.mp3")

        audio_file = open("coach.mp3", "rb")
        audio_bytes = audio_file.read()

        st.audio(audio_bytes, format="audio/mp3")

    except:
        pass

# ============================================================
# PAGE 1 - ACCUEIL
# ============================================================
if st.session_state.step == 0:

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:

        if os.path.exists("machine.jpg"):
            st.image("machine.jpg", width=450)
        else:
            st.warning("Ajoute le fichier machine.jpg dans ton projet.")

    with col2:

        st.title("🎾  Tennis BOT")

        st.markdown("""
### Machine intelligente d'entraînement

Cette machine de distribution de balles permet :

- ⚡ d'adapter automatiquement la vitesse
- 🌀 de modifier les effets de balle
- 🎯 d'améliorer la précision du joueur
- 🤖 d'obtenir des conseils grâce à un Coach IA

Le système analyse votre niveau et ajuste les paramètres
pour proposer un entraînement personnalisé.

### 🔥 Prêt à commencer votre entraînement ?
""")

    c1, c2, c3 = st.columns([1,2,1])

    with c2:
        if st.button(
            "🚀 Démarrer l'expérience",
            use_container_width=True
        ):
            st.session_state.step = 1
            st.rerun()

# ============================================================
# PAGE 2 - FORMULAIRE
# ============================================================
elif st.session_state.step == 1:

    st.title("📝 Profil Joueur")

    if st.button("⬅ Retour à l'accueil"):
        st.session_state.step = 0
        st.rerun()

    st.markdown("---")

    with st.form("formulaire_joueur"):

        nom = st.text_input("👤 Nom")

        age = st.text_input("🎂 Âge")

        frequence = st.selectbox(
            "📅 Fréquence de jeu",
            [
                "1 fois par semaine",
                "2 fois par semaine",
                "3-4 fois par semaine",
                "5-6 fois par semaine",
                "Tous les jours"
            ]
        )

        anciennete = st.selectbox(
            "🎾 Ancienneté",
            [
                "< 1 an",
                "1 an",
                "2 ans",
                "3 à 5 ans",
                "5+ ans"
            ]
        )

        niveau = st.selectbox(
            "🏆 Niveau",
            [
                "Débutant",
                "Intermédiaire",
                "Avancé"
            ]
        )

        valider = st.form_submit_button(
            "✅ Valider mes informations"
        )

        if valider and nom:

            base_speed = {
                "Débutant":60,
                "Intermédiaire":85,
                "Avancé":110
            }[niveau]

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

    user = st.session_state.user

    st.success(f"Bienvenue {user['Nom']} 🎾")

    col1, col2 = st.columns([1, 1])

    with col1:

        speed = st.slider(
            "⚡ Vitesse de la balle",
            30,
            150,
            user["base_speed"]
        )

        spin = st.slider(
            "🌀 Effet",
            0,
            15,
            5
        )

        if st.button(
            "🎾 Lancer la balle",
            use_container_width=True
        ):

            x = np.random.normal(0, 4)

            precision = round(abs(x) * 2, 2)

            zone = "OK" if precision < 6 else "MISS"

            st.session_state.history.append({
                "Vitesse": speed,
                "Effet": spin,
                "Précision": precision,
                "Résultat": zone
            })

            message = coach(
                speed,
                spin,
                precision,
                user["Niveau"]
            )

            st.markdown("### 🤖 Coach IA")
            st.info(message)

            speak(message)

    with col2:

        fig = go.Figure()

        fig.add_trace(go.Scatter3d(
            x=[0, 0, np.random.uniform(-3, 3)],
            y=[0, 8, 14],
            z=[0, 2, 0],
            mode="lines+markers",
            line=dict(width=8),
            marker=dict(size=6)
        ))

        fig.update_layout(
            title="🎾 Simulation 3D de la trajectoire",
            height=500,
            margin=dict(l=0, r=0, b=0, t=40)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.markdown("---")

    colA, colB = st.columns(2)

    with colA:
        if st.button(
            "📊 Voir l'historique",
            use_container_width=True
        ):
            st.session_state.step = 3
            st.rerun()

    with colB:
        if st.button(
            "🔄 Nouveau joueur",
            use_container_width=True
        ):
            reset_all()

# ============================================================
# PAGE 4 - HISTORIQUE
# ============================================================
elif st.session_state.step == 3:

    st.title("📊 Historique des tirs")

    if len(st.session_state.history) > 0:

        df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total tirs",
                len(df)
            )

        with col2:
            st.metric(
                "Précision moyenne",
                round(df["Précision"].mean(), 2)
            )

        with col3:

            taux = (
                (df["Résultat"] == "OK").mean()
                * 100
            )

            st.metric(
                "Réussite",
                f"{taux:.1f}%"
            )

        st.markdown("### 📈 Évolution des performances")

        fig_hist = go.Figure()

        fig_hist.add_trace(
            go.Scatter(
                y=df["Précision"],
                mode="lines+markers",
                name="Précision"
            )
        )

        fig_hist.update_layout(
            height=400
        )

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

    else:
        st.info("Aucun tir enregistré.")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button(
            "⬅ Retour au jeu",
            use_container_width=True
        ):
            st.session_state.step = 2
            st.rerun()

    with col2:
        if st.button(
            "🔄 Nouveau joueur",
            use_container_width=True
        ):
            reset_all()

    with col3:
        if st.button(
            "🚪 Quitter",
            use_container_width=True
        ):
            st.stop()

# ============================================================
# FOOTER
# ============================================================
st.markdown("""
<hr style="border:1px solid rgba(255,255,255,0.3);">

<div class="footer">
🎾 Tennis BOT<br>
Developpée par Nouhaila Bahi & Zainab Edrif
</div>
""", unsafe_allow_html=True)
