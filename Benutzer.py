import json

import requests

from models import Sensor_data, UpdateDataModel

# TODO: Wie erhalten wir für uns interessante Informationen von der Verwaltung?
# TODO: Was sind interessante Daten und welche benötigen wir unter Umständen gar nicht?
# TODO: Wie gehen wir mit beschädigten bzw. falschen Informationen um?
# TODO: Wie stellen wir die Informationen bestmöglich für den Nutzer da?

if __name__ == '__main__':
    data = Sensor_data(name="Test")
    new_data = UpdateDataModel(name="Updated Test")
    answer1 = requests.post("http://127.0.0.1:8000/data/", data.json())
    answer2 = requests.put(f"http://127.0.0.1:8000/data/{json.loads(answer1.content)['_id']}", new_data.json())
    answer3 = requests.delete(f"http://127.0.0.1:8000/data/{json.loads(answer1.content)['_id']}")
    answer4 = requests.get(f"http://127.0.0.1:8000/data/{json.loads(answer1.content)['_id']}")
    print(answer1.content)
    print(answer2.content)
    print(answer3.content)
    print(answer4.content)