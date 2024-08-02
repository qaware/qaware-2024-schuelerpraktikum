import pandas as pd
import numpy as np


# Funktion zum Generieren von realistischeren Testdaten
def generate_realistic_test_data(sensor_name, category, num_points, start_timestamp, pressure_mean, temperature_mean):
    test_data = []
    for i in range(num_points):
        test_data.append({
            "name": sensor_name,
            "type": category,
            "pressure": np.random.normal(pressure_mean, 0.05),  # Druck um den Mittelwert mit geringer Variation
            "temperature": np.random.normal(temperature_mean, 2),  # Temperatur um den Mittelwert mit Variation
            "timestamp": start_timestamp + i * 10  # Erhöhen Sie den Zeitstempel in festen Intervallen
        })
    return test_data


# Mehr Testdaten generieren
realistic_test_data = {
    "thruster": {
        "thruster_3.b": generate_realistic_test_data("thruster_3.b", "thruster", 20, 12887729, 0.5, 50),
        "thruster_3.a": generate_realistic_test_data("thruster_3.a", "thruster", 20, 12887729, 0.6, 55),
        "thruster_4.a": generate_realistic_test_data("thruster_4.a", "thruster", 20, 12887729, 0.55, 53)
    },
    "gas_valve": {
        "gas_valve_3.b": generate_realistic_test_data("gas_valve_3.b", "gas_valve", 20, 12887729, 0.3, 40),
        "gas_valve_3.a": generate_realistic_test_data("gas_valve_3.a", "gas_valve", 20, 12887729, 0.35, 42),
        "gas_valve_4.a": generate_realistic_test_data("gas_valve_4.a", "gas_valve", 20, 12887729, 0.32, 41)
    }
}

print(realistic_test_data)


def reformat_data(data):
    # List to store the reformatted data
    reformatted_data = []

    # Iterate through the main categories
    for type, sensor_names in data.items():
        # Iterate through the sensor_names
        for name, data_records in sensor_names.items():
            # Iterate through each record in the subcategory
            for record in data_records:
                reformatted_record = {
                    "name": name,
                    "type": type,
                    "pressure": record["pressure"],
                    "temperature": record["temperature"],
                    "timestamp": record["timestamp"]
                }
                reformatted_data.append(reformatted_record)

    # Convert the list of dictionaries to a Pandas DataFrame
    df = pd.DataFrame(reformatted_data)
    return df
