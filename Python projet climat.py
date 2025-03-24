import random
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Initialisation des variables avec session_state
if 'temperature' not in st.session_state:
    st.session_state.temperature = 14.0  # Seuil initial réaliste
    st.session_state.co2_level = 400
    st.session_state.score = 100
    st.session_state.annees = []
    st.session_state.temperatures = []
    st.session_state.co2_levels = []
    st.session_state.game_over = False  # Variable pour bloquer la partie en cas de défaite

# Événements aléatoires possibles
evenements_aleatoires = [
    ("Développement technologique", -15),
    ("Éruption volcanique", +20),
    ("Campagne de reforestation mondiale", -20),
    ("Catastrophe naturelle", +10),
]

# Fonction pour appliquer les décisions de l'utilisateur
def appliquer_decision(action):
    actions = {
        "Réduire les émissions de CO₂": (-25, +8),
        "Planter des arbres": (-10, +5),
        "Investir dans les énergies renouvelables": (-20, +7),
        "Ne rien faire": (+15, -10),
    }
    co2_change, score_change = actions[action]
    st.session_state.co2_level += co2_change
    st.session_state.score += score_change
    st.session_state.temperature += (st.session_state.co2_level - 400) * 0.006  # Facteur de réchauffement ajusté

# Fonction pour gérer les événements aléatoires
def evenement_aleatoire():
    evenement, co2_impact = random.choice(evenements_aleatoires)
    st.write(f"**Événement aléatoire :** {evenement} ! CO₂ modifié de {co2_impact} ppm.")
    st.session_state.co2_level += co2_impact

# Fonction pour tracer les graphiques
def tracer_graphiques():
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.plot(st.session_state.annees, st.session_state.temperatures, color="red", label="Température (°C)")
    plt.xlabel("Années")
    plt.ylabel("Température (°C)")
    plt.title("Évolution de la Température Globale")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(st.session_state.annees, st.session_state.co2_levels, color="green", label="Niveau de CO₂ (ppm)")
    plt.xlabel("Années")
    plt.ylabel("Niveau de CO₂ (ppm)")
    plt.title("Évolution du CO₂")
    plt.legend()

    plt.tight_layout()
    st.pyplot(plt)

# Interface Streamlit
st.title("Simulation du Réchauffement Climatique 🌍")

# Vérifier si la partie est terminée et bloquer les actions
if not st.session_state.game_over:
    st.write("Prenez des décisions chaque année pour limiter le réchauffement climatique.")
    st.write("L'objectif est de stabiliser la température mondiale avant qu'elle n'atteigne **16°C** et de maintenir un score positif.")

    # Affichage des paramètres actuels
    st.write(f"**Température actuelle :** {st.session_state.temperature:.2f}°C")
    st.write(f"**Niveau de CO₂ :** {st.session_state.co2_level} ppm")
    st.write(f"**Score :** {st.session_state.score}")

    # Sélection de l'action
    action = st.radio("Choisissez une action :", [
        "Réduire les émissions de CO₂",
        "Planter des arbres",
        "Investir dans les énergies renouvelables",
        "Ne rien faire"
    ])

    if st.button("Valider l'action"):
        appliquer_decision(action)

        # Ajouter les données actuelles à l'historique
        st.session_state.annees.append(len(st.session_state.annees) + 1)
        st.session_state.temperatures.append(st.session_state.temperature)
        st.session_state.co2_levels.append(st.session_state.co2_level)

        # Événement aléatoire avec 30 % de probabilité
        if random.random() < 0.3:
            evenement_aleatoire()

        # Conditions de fin du jeu
        if st.session_state.temperature >= 16.0:
            st.session_state.game_over = True
            st.error("La température a dépassé 16°C. Vous avez perdu !")
        elif st.session_state.score <= 0:
            st.session_state.game_over = True
            st.error("Votre score est tombé à zéro. Vous avez perdu !")
        elif st.session_state.co2_level >= 550:
            st.session_state.game_over = True
            st.error("Le niveau de CO₂ a dépassé 550 ppm. Vous avez perdu !")
        else:
            st.success("Action prise en compte. Continuez à jouer !")

        tracer_graphiques()
else:
    st.title("🎮 Fin de la Partie")
    st.write("La partie est terminée. Voici vos résultats :")
    st.write(f"**Température finale :** {st.session_state.temperature:.2f}°C")
    st.write(f"**Niveau de CO₂ final :** {st.session_state.co2_level} ppm")
    st.write(f"**Score final :** {st.session_state.score}")

    tracer_graphiques()

    # Sauvegarde des résultats dans un DataFrame Pandas
    data = {
        "Année": st.session_state.annees,
        "Température (°C)": st.session_state.temperatures,
        "Niveau de CO₂ (ppm)": st.session_state.co2_levels
    }
    df = pd.DataFrame(data)
    st.write("## Historique des données")
    st.dataframe(df)

    # Télécharger les résultats en CSV
    st.download_button(
        label="Télécharger les résultats en CSV",
        data=df.to_csv(index=False),
        file_name="simulation_climatique.csv",
        mime="text/csv"
    )
