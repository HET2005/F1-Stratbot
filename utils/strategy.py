import pandas as pd

TOTAL_LAPS = 70  

# Base lap times per track (avg in seconds)
track_baseline = {
    "Silverstone": 90,
    "Monaco": 75,
    "Monza": 80,
    "Spa": 92,
    "Suzuka": 88,
    "Hungaroring": 85,
    "Zandvoort": 87,
    "Yas Marina": 89,
    "Imola": 86,
    "Barcelona": 84,
}

# Driver adjustments
driver_adjustments = {
    "Verstappen": -1.5,
    "Perez": +0.5,
    "Hamilton": -1.0,
    "Russell": -0.3,
    "Leclerc": -0.7,
    "Sainz": -0.2,
}

# Team modifiers
team_modifiers = {
    "Red Bull": -0.5,
    "Mercedes": -0.2,
    "Ferrari": +0.3
}


aero_modifiers = {
    "High": -0.3,       # high downforce = better corners
    "Balanced": 0.0,
    "Low": +0.3         # low downforce = faster straights, but trickier handling
}

tyre_multipliers = {
    "Soft": -0.8,
    "Medium": 0,
    "Hard": +0.8,
}
def simulate_strategy(strategy, driver, track, aero):
    base_time = track_baseline.get(track, 90)   # default 90 if track not listed
    driver_adj = driver_adjustments.get(driver, 0)

    aero_adj = {
        "High": -0.5,
        "Balanced": 0,
        "Low": +0.5
    }.get(aero, 0)

    laps_done = 0
    stint_num = 0
    results = []

    for tyre, stint_length in strategy:
        stint_num += 1
        tyre_adj = tyre_multipliers.get(tyre, 0)

        for lap in range(stint_length):
            laps_done += 1
            if laps_done > TOTAL_LAPS:
                break

            lap_time = base_time + driver_adj + tyre_adj + aero_adj + (lap * 0.01)
            results.append({
                "lap": laps_done,
                "stint": stint_num,
                "tyre": tyre,
                "lap_time": lap_time
            })

    df = pd.DataFrame(results)
    total_time = df["lap_time"].sum()

    return df, total_time
