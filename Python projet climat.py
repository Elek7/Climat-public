import random
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

temperature = 14.0
co2 = 400
score = 100
temperature_max = 19.0
temperature_min = -20.0 
annees, temperatures, co2_niveaux, scores = [], [], [], []
jeu_termine = False

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

if not jeu_termine:
    st.write(f"Température actuelle : {temperature:.2f}°C")
    st.write(f"Niveau de CO₂ : {co2} ppm")
    st.write(f"Score : {score}")
    
    choix_action = st.radio("Quelle action souhaitez-vous entreprendre cette année ?", list(actions.keys()))

    if st.button("Valider l'action"):
        effet_co2, effet_score = actions[choix_action]
        co2 += effet_co2
        score += effet_score
        if random.random() < 0.3:
            evenement, impact = random.choice(evenements)
            co2 += impact
            st.write(f"Événement : {evenement} ({impact} ppm)")
        temperature += (co2 - 400) * 0.008
        temperature = max(min(temperature, temperature_max), temperature_min)
        annees.append(len(annees) + 1)
        temperatures.append(temperature)
        co2_niveaux.append(co2)
        scores.append(score)

        if temperature >= temperature_max:
            jeu_termine = True
            st.error("La température a dépassé 19°C. Défaite.")
        elif temperature <= temperature_min:
            jeu_termine = True
            st.error("La Terre est devenue trop froide. Défaite.")
        elif score <= 0:
            jeu_termine = True
            st.error("Votre score est tombé à 0. Défaite.")
        elif len(annees) >= 50 and temperature < temperature_max:
            jeu_termine = True
            st.success("Vous avez réussi à maintenir une température stable. Victoire.")
    
else:
    st.error("La partie est terminée.")
    
fig, ax = plt.subplots(1, 2, figsize=(12, 5))
ax[0].plot(annees, temperatures, color="red")
ax[0].set_title("Évolution de la Température")
ax[0].set_xlabel("Années")
ax[0].set_ylabel("Température (°C)")
ax[1].plot(annees, co2_niveaux, color="green")
ax[1].set_title("Évolution du CO₂")
ax[1].set_xlabel("Années")
ax[1].set_ylabel("CO₂ (ppm)")
st.pyplot(fig)

donnees = pd.DataFrame({
    "Année": annees,
    "Température (°C)": temperatures,
    "CO₂ (ppm)": co2_niveaux,
    "Score": scores
})

st.dataframe(donnees)
st.download_button("Télécharger les résultats", donnees.to_csv(index=False), "resultats_climat.csv", "text/csv")
