import pandas as pd
import numpy as np


# Funktion zum Generieren von realistischeren Testdaten mit Trends
def generate_realistic_test_data_with_trend(sensor_name, category, num_points, start_timestamp, pressure_mean, temperature_mean, pressure_trend, temperature_trend):
    data = []
    for i in range(num_points):
        data.append({
            "name": sensor_name,
            "type": category,
            "pressure": np.random.normal(pressure_mean + i * pressure_trend, 0.05),  # Druck mit einem Trend
            "temperature": np.random.normal(temperature_mean + i * temperature_trend, 2),  # Temperatur mit einem Trend
            "timestamp": start_timestamp + i * 10  # Erhöhen Sie den Zeitstempel in festen Intervallen
        })
    return data

# Mehr realistischere Testdaten mit Trends generieren
data = {
    "thruster": {
        "thruster_3.b": generate_realistic_test_data_with_trend("thruster_3.b", "thruster", 50, 12887729, 0.5, 50, 0.001, 0.1),
        "thruster_3.a": generate_realistic_test_data_with_trend("thruster_3.a", "thruster", 50, 12887729, 0.6, 55, 0.001, 0.1),
        # "thruster_4.a": generate_realistic_test_data_with_trend("thruster_4.a", "thruster", 50, 12887729, 0.55, 53, 0.001, 0.1)
    },
    "gas_valve": {
        "gas_valve_3.b": generate_realistic_test_data_with_trend("gas_valve_3.b", "gas_valve", 50, 12887729, 0.3, 40, 0.0005, 0.05),
        # "gas_valve_3.a": generate_realistic_test_data_with_trend("gas_valve_3.a", "gas_valve", 50, 12887729, 0.35, 42, 0.0005, 0.05),
        "gas_valve_4.a": generate_realistic_test_data_with_trend("gas_valve_4.a", "gas_valve", 50, 12887729, 0.32, 41, 0.0005, 0.05)
    }
}

print(data)


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
