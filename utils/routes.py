from flask import Blueprint, render_template, request

main = Blueprint("main", __name__)

@main.route("/")
def intro():
    return render_template("intro.html")

@main.route("/home")
def home():
    return render_template("index.html")

@main.route("/strategy", methods=["GET", "POST"])
def strategy():
    result = None

    teams = ["Red Bull", "Ferrari", "Mercedes", "McLaren"]
    drivers = {
        "Red Bull": ["Max Verstappen", "Sergio Perez"],
        
        "Ferrari": ["Charles Leclerc", "Carlos Sainz"],
        "Mercedes": ["Lewis Hamilton", "George Russell"],
        "McLaren": ["Lando Norris", "Oscar Piastri"]
    }

    if request.method == "POST":
        team = request.form.get("team")
        driver = request.form.get("driver")
        track = request.form.get("track")
        aero = request.form.get("aero")
        tyres = [request.form.get(f"tyre{i}") for i in range(1, 4)]
        laps = [int(request.form.get(f"lap{i}", 0)) for i in range(1, 4)]

        # Dummy strategy score logic
        time = 3600
        tyre_speed = {"Soft": -40, "Medium": -20, "Hard": 0}
        aero_boost = {"High": 20, "Balanced": 10, "Low": -10}

        for tyre in tyres:
            time += tyre_speed.get(tyre, 0)

        time -= aero_boost.get(aero, 0)

        skill_map = {
            "Max Verstappen": 95, "Sergio Perez": 85,
            "Charles Leclerc": 90, "Carlos Sainz": 86,
            "Lewis Hamilton": 92, "George Russell": 87,
            "Lando Norris": 88, "Oscar Piastri": 83
        }
        time -= skill_map.get(driver, 80)

        result = f"Estimated Time: {time} sec - Strategy looks {'Aggressive' if 'Soft' in tyres else 'Conservative'}"

    return render_template("strategy.html", result=result, teams=teams, drivers=drivers)


@main.route("/ranking")
def ranking():
    drivers = [
        {"name": "Max Verstappen", "team": "Red Bull", "mu": 35, "sigma": 3},
        {"name": "Charles Leclerc", "team": "Ferrari", "mu": 30, "sigma": 4},
        {"name": "Lewis Hamilton", "team": "Mercedes", "mu": 32, "sigma": 3.5},
        {"name": "Lando Norris", "team": "McLaren", "mu": 28, "sigma": 4},
        {"name": "Fernando Alonso", "team": "Aston Martin", "mu": 29, "sigma": 3},
        {"name": "George Russell", "team": "Mercedes", "mu": 27, "sigma": 4},
        {"name": "Sergio Perez", "team": "Red Bull", "mu": 26, "sigma": 4.5},
        {"name": "Carlos Sainz", "team": "Ferrari", "mu": 25, "sigma": 3.5},
        {"name": "Oscar Piastri", "team": "McLaren", "mu": 24, "sigma": 4},
        {"name": "Pierre Gasly", "team": "Alpine", "mu": 22, "sigma": 4},
    ]

    # Sort using TrueSkill formula: mu - 3 * sigma
    ranked = sorted(drivers, key=lambda x: x["mu"] - 3 * x["sigma"], reverse=True)

    # Prepare data for chart
    names = [d["name"] for d in ranked]
    scores = [round(d["mu"] - 3 * d["sigma"], 2) for d in ranked]

    return render_template("ranking.html", ranked=ranked, names=names, scores=scores)


@main.route("/predictor", methods=["GET", "POST"])
def predictor():
    result = None
    confidence = None

    if request.method == "POST":
        team = request.form.get("team")
        track = request.form.get("track")

        # 🧠 Dummy prediction logic
        if team == "Red Bull" and track == "Silverstone":
            result = "Red Bull"
            confidence = 86
        elif team == "Ferrari" and track == "Monaco":
            result = "Ferrari"
            confidence = 78
        else:
            result = "Mercedes"
            confidence = 65

    return render_template("predictor.html", result=result, confidence=confidence)
