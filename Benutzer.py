import json
import time
URL = "http://127.0.0.1:8000"

import requests

from models import SensorData, UpdateDataModel

# TODO: Wie erhalten wir für uns interessante Informationen von der Verwaltung?
# TODO: Was sind interessante Daten und welche benötigen wir unter Umständen gar nicht?
# TODO: Wie gehen wir mit beschädigten bzw. falschen Informationen um?
# TODO: Wie stellen wir die Informationen bestmöglich für den Nutzer da?

if __name__ == '__main__':
    sens_data = SensorData(value=1.10, name="Test", data_type="bla", time=123)
    sens_data2 = SensorData(value=1.10, name="Test", data_type="bla", time=123)
    answer1 = requests.post("http://127.0.0.1:8000/data/addData/", sens_data.json())
    answer2 = requests.get(f"{URL}/data/doesExist/{sens_data2.data_type}/{sens_data2.name}/{sens_data2.time}")
    print(answer1.content)
    print(answer2.content)
    answer3 = requests.get(f"{URL}/data/get/bla")
    print(answer3.content)
