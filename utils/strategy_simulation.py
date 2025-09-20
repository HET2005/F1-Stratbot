# utils/strategy_simulation.py

import pandas as pd

def simulate_strategy(model, strategy, driver_id, race_id, pit_stop_time=22):
    lap_counter = 1
    stint_number = 1
    all_predictions = []

    for i, (compound, stint_length) in enumerate(strategy):
        for _ in range(stint_length):
            sample = {
                'lap': lap_counter,
                'stint': stint_number,
                'tyre': compound,
                'driver_id': driver_id,
                'race_id': race_id
            }
            X = pd.DataFrame([sample])
            predicted_lap_time = model.predict(X)[0]

            all_predictions.append({
                'lap': lap_counter,
                'stint': stint_number,
                'tyre': compound,
                'lap_time': predicted_lap_time
            })

            lap_counter += 1

        if i < len(strategy) - 1:
            all_predictions.append({
                'lap': lap_counter,
                'stint': stint_number,
                'tyre': 'PIT',
                'lap_time': pit_stop_time
            })
            lap_counter += 1
            stint_number += 1

    df_predictions = pd.DataFrame(all_predictions)
    total_time = df_predictions['lap_time'].sum()
    return df_predictions, total_time
