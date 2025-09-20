import pandas as pd
from utils.strategy import simulate_strategy
from utils.predictor import predict_winner
from utils.ranking import calculate_driver_rankings
from flask import Flask, Blueprint, render_template, request

app = Flask(__name__)

# --------------------------
# Load CatBoost model
# --------------------------

# Dummy team-driver mapping
team_driver_map = {
    "Red Bull": ["Verstappen", "Perez"],
    "Mercedes": ["Hamilton", "Russell"],
    "Ferrari": ["Leclerc", "Sainz"],
    "McLaren": ["Norris", "Piastri"],
    "Aston Martin": ["Alonso", "Stroll"],
    "Alpine": ["Ocon", "Gasly"],
    "Williams": ["Albon", "Sargeant"],
    "Haas": ["Magnussen", "Hülkenberg"],
    "RB": ["Ricciardo", "Tsunoda"],
    "Sauber": ["Bottas", "Zhou"]
}

# --------------------------
# ROUTES
# --------------------------

@app.route('/')
def index():
    return render_template('intro.html')


@app.route('/home')
def home_page():
    return render_template('index.html')


@app.route('/strategy', methods=['GET', 'POST'])
def strategy_page():
    if request.method == 'POST':
        driver = request.form['driver']
        track = request.form['track']

        # Build tyre strategy from form
        strategy = []
        previous_lap = 0
        for i in range(1, 4):
            tyre = request.form[f'tyre{i}']
            lap = int(request.form[f'lap{i}'])
            stint_length = lap - previous_lap
            strategy.append((tyre, stint_length))
            previous_lap = lap

        # Run simulation
# Include aero from form
        aero = request.form['aero']

# Run simulation
        df_results, total_time = simulate_strategy(strategy, driver, track, aero)

        # Calculate fastest lap
        fastest_lap = round(df_results["lap_time"].min(), 2)

        # Average lap time per stint
        avg_stint_times = (
            df_results.groupby("stint")["lap_time"].mean().round(2).tolist()
        )
        stints = df_results["stint"].unique().tolist()

        return render_template(
            "strategy.html",
            teams=list(team_driver_map.keys()),
            drivers=team_driver_map,
            result=f"{round(total_time/60, 2)} minutes",  # total race time in minutes
            df_results=df_results.to_dict(orient="records"),
            fastest_lap=fastest_lap,
            avg_stint_times=avg_stint_times,
            stints=stints,
            selected_driver=driver,
            selected_track=track,
        )

    return render_template(
        "strategy.html",
        teams=list(team_driver_map.keys()),
        drivers=team_driver_map
    )


@app.route('/predictor', methods=['GET', 'POST'])
def predictor_page():
    if request.method == 'POST':
        team = request.form['team']
        track = request.form['track']

        winner, confidence = predict_winner(team, track)

        return render_template('predictor.html', result=winner, confidence=confidence)

    return render_template('predictor.html')


@app.route("/ranking")
def ranking():
    df = calculate_driver_rankings("dataset/driver_ranking.csv")

    # Extract names and scores for chart
    names = df["surname"].tolist()
    scores = df["points"].tolist()
    year = df["year"].max() if "year" in df.columns else "Latest"

    return render_template(
        "ranking.html",
        ranking=df.to_dict(orient="records"),
        names=names,
        scores=scores,
        year=year
    )

# --------------------------
# Main entry
# --------------------------
if __name__ == '__main__':
    app.run(debug=True)
