import random
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Paramètres initiaux
temp_min = -273.15
temp_max = 16.0
co2_max = 550
co2_init = 400

game_state = {
    "temperature": 14.0,
    "co2": co2_init,
    "score": 100,
    "annees": [],
    "temperatures": [],
    "co2_levels": [],
    "game_over": False
}

actions = {
    "Réduire CO₂": (-25, 8),
    "Planter des arbres": (-10, 5),
    "Énergies renouvelables": (-20, 7),
    "Ne rien faire": (15, -10)
}

events = [
    ("Développement technologique", -15),
    ("Éruption volcanique", 20),
    ("Reforestation mondiale", -20),
    ("Catastrophe naturelle", 10)
]

title("Simulation du Climat 🌍")

if not game_state["game_over"]:
    write(f"Température : {game_state['temperature']:.2f}°C | CO₂ : {game_state['co2']} ppm | Score : {game_state['score']}")
    action = radio("Choisissez une action :", list(actions.keys()))
    
    if button("Valider"):
        co2_change, score_change = actions[action]
        game_state["co2"] += co2_change
        game_state["score"] += score_change
        game_state["temperature"] = max(temp_min, 14.0 + (game_state["co2"] - co2_init) * 0.006)
        
        if random.random() < 0.3:
            event, co2_impact = random.choice(events)
            game_state["co2"] += co2_impact
            write(f"**Événement :** {event} ({co2_impact} ppm)")
        
        game_state["annees"].append(len(game_state["annees"]) + 1)
        game_state["temperatures"].append(game_state["temperature"])
        game_state["co2_levels"].append(game_state["co2"])
        
        if game_state["temperature"] >= temp_max or game_state["co2"] >= co2_max or game_state["score"] <= 0:
            game_state["game_over"] = True
        
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        ax[0].plot(game_state["annees"], game_state["temperatures"], 'r-', label="Température (°C)")
        ax[1].plot(game_state["annees"], game_state["co2_levels"], 'g-', label="CO₂ (ppm)")
        for a in ax:
            a.legend()
            a.set_xlabel("Années")
        pyplot(fig)
else:
    error("Partie terminée ! Voici vos résultats :")
    fig, ax = plt.subplots(1, 2, figsize=(10, 5))
    ax[0].plot(game_state["annees"], game_state["temperatures"], 'r-', label="Température (°C)")
    ax[1].plot(game_state["annees"], game_state["co2_levels"], 'g-', label="CO₂ (ppm)")
    for a in ax:
        a.legend()
        a.set_xlabel("Années")
    pyplot(fig)
    
    df = pd.DataFrame({"Année": game_state["annees"], "Température (°C)": game_state["temperatures"], "CO₂ (ppm)": game_state["co2_levels"]})
    download_button("Télécharger les résultats", df.to_csv(index=False), "resultats_climat.csv", "text/csv")
