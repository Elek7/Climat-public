import random
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

if "temperature" not in st.session_state:
    st.session_state.temperature = 14.0
    st.session_state.co2 = 400
    st.session_state.score = 100
    st.session_state.temperature_max = 19.0
    st.session_state.temperature_min = -20.0
    st.session_state.annees = []
    st.session_state.temperatures = []
    st.session_state.co2_niveaux = []
    st.session_state.scores = []
    st.session_state.jeu_termine = False

actions = {
    "Réduire les émissions de CO₂": (-30, 8),
    "Planter des arbres": (-15, 5),
    "Investir dans les énergies renouvelables": (-25, 7),
    "Ne rien faire": (20, -10)
}

evenements = [
    ("Développement technologique", -20),
    ("Éruption volcanique", 25),
    ("Campagne de reforestation mondiale", -30),
    ("Catastrophe naturelle", 10)
]

st.title("Simulation de l'Évolution du Climat")

if st.session_state.jeu_termine:
    st.error("La partie est terminée.")
else:
    st.write(f"Température actuelle : {st.session_state.temperature:.2f}°C")
    st.write(f"Niveau de CO₂ : {st.session_state.co2} ppm")
    st.write(f"Score : {st.session_state.score}")

    choix_action = st.radio("Quelle action souhaitez-vous entreprendre cette année ?", list(actions.keys()))

    if st.button("Valider l'action"):
        effet_co2, effet_score = actions[choix_action]
        st.session_state.co2 += effet_co2
        st.session_state.score += effet_score
        
        if random.random() < 0.3:
            evenement, impact = random.choice(evenements)
            st.session_state.co2 += impact
            st.write(f"Événement : {evenement} ({impact} ppm)")

        st.session_state.temperature += (st.session_state.co2 - 400) * 0.008
        st.session_state.temperature = max(min(st.session_state.temperature, st.session_state.temperature_max), st.session_state.temperature_min)

        st.session_state.annees.append(len(st.session_state.annees) + 1)
        st.session_state.temperatures.append(st.session_state.temperature)
        st.session_state.co2_niveaux.append(st.session_state.co2)
        st.session_state.scores.append(st.session_state.score)

        if st.session_state.temperature >= st.session_state.temperature_max:
            st.session_state.jeu_termine = True
            st.error("La température a dépassé 19°C. Défaite.")
        elif st.session_state.temperature <= st.session_state.temperature_min:
            st.session_state.jeu_termine = True
            st.error("La Terre est devenue trop froide. Défaite.")
        elif st.session_state.score <= 0:
            st.session_state.jeu_termine = True
            st.error("Votre score est tombé à 0. Défaite.")
        elif len(st.session_state.annees) >= 50 and st.session_state.temperature < st.session_state.temperature_max:
            st.session_state.jeu_termine = True
            st.success("Vous avez réussi à maintenir une température stable. Victoire.")

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].plot(st.session_state.annees, st.session_state.temperatures, color="red")
ax[0].set_title("Évolution de la Température")
ax[0].set_xlabel("Années")
ax[0].set_ylabel("Température (°C)")
ax[1].plot(st.session_state.annees, st.session_state.co2_niveaux, color="green")
ax[1].set_title("Évolution du CO₂")
ax[1].set_xlabel("Années")
ax[1].set_ylabel("CO₂ (ppm)")
st.pyplot(fig)

donnees = pd.DataFrame({
    "Année": st.session_state.annees,
    "Température (°C)": st.session_state.temperatures,
    "CO₂ (ppm)": st.session_state.co2_niveaux,
    "Score": st.session_state.scores
})

st.dataframe(donnees)
st.download_button("Télécharger les résultats", donnees.to_csv(index=False), "resultats_climat.csv", "text/csv")

if st.button("Recommencer une partie"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()
