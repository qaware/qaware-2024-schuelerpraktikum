import datetime
import json
import os.path
import random
import time

BASE_PATH = path = os.path.dirname(os.path.dirname(__file__))


class SensorKey:
    """Unique key of a sensor"""

    def __init__(self, name: str, type: str):
        """Constructor"""
        self.name: str = name
        self.type: str = type


class Sensor:
    """Sensor object, which stores all information of a given sensor."""

    def __init__(self, name: str, data_type: str, value: float, time: int):
        """Constructor"""

        self.name = name
        self.data_type = data_type
        self.value = value
        self.time = time


class DataGenerator:
    """Data Generator, which provides and stores sensor data of a given satellite."""

    def __init__(self):
        """Constructor"""
        self.available_sensors: list[SensorKey] = [
            SensorKey(name="thruster_1.a", type="thruster"),
            SensorKey(name="thruster_1.b", type="thruster"),
            SensorKey(name="thruster_1.c", type="thruster"),
            # SensorKey(name="thruster_2.a", type="thruster"),
            # SensorKey(name="thruster_2.b", type="thruster"),
            # SensorKey(name="thruster_2.c", type="thruster"),
            # SensorKey(name="thruster_3.a", type="thruster"),
            # SensorKey(name="thruster_3.b", type="thruster"),
            # SensorKey(name="thruster_3.c", type="thruster"),
            SensorKey(name="oxygen_tank_1", type="gas_valve"),
            SensorKey(name="oxygen_tank_2", type="gas_valve"),
            SensorKey(name="hydrogen_tank_1", type="gas_valve"),
            # SensorKey(name="hydrogen_tank_2", type="gas_valve")
        ]

    def generate_new_sensor_data(self):

        selected_key_idx = random.randint(0, len(self.available_sensors) - 1)
        selected_key = self.available_sensors[selected_key_idx]

        if selected_key.type == 'gas_valve':
            value = random.uniform(0.5, 9.0)
        elif selected_key.type == 'thruster':
            value = random.uniform(200,500)

        sensor_data = Sensor(
            name=selected_key.name,
            data_type=selected_key.type,
            value=value,
            time=int(time.time())
        )

        er  = random.randint(0,4)
        if er == 0:
            er = random.randint(0,3)
            if er == 0:
                sensor_data.name = None
            elif er == 1:
                sensor_data.data_type = None
            elif er == 2:
                sensor_data.value = None
            else:
                sensor_data.time = None

        return sensor_data

    @staticmethod
    def store_sensor_data(data: Sensor):
        content = data.__dict__
        er = random.randint(0,4)
        if er == 0:
            er = random.randint(0,3)
            if er == 0:
                content.pop('name')
            elif er == 1:
                content.pop('data_type')
            elif er == 2:
                content.pop('time')
            else:
                content.pop('value')
        file_name = "/data/TM_" + datetime.datetime.now().isoformat() + ".json"
        if not os.path.exists(BASE_PATH+ "/data/"):
            os.makedirs(BASE_PATH+ "/data/")
        with open(BASE_PATH + file_name, "w") as file:
            json.dump(content, file)


if __name__ == '__main__':
    generator = DataGenerator()

    while True:
        data = generator.generate_new_sensor_data()
        generator.store_sensor_data(data=data)
        print(f"Sucessfully stored: {data}")
        time.sleep(0.5)
