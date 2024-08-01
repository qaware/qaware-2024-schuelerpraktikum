import pandas as pd


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

