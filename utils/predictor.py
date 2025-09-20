import random

def predict_winner(team, track):
    teams = {
        "Red Bull": ["Verstappen", "Perez"],
        "Mercedes": ["Hamilton", "Russell"],
        "Ferrari": ["Leclerc", "Sainz"],
        "McLaren": ["Norris", "Piastri"]
    }

    # Pick random driver from team
    drivers = teams.get(team, ["Unknown"])
    predicted_driver = random.choice(drivers)

    # Simulated confidence
    confidence = round(random.uniform(70, 99), 2)

    return predicted_driver, confidence
