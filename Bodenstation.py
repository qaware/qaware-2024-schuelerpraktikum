import json
import os
import requests

from models import Sensor_data, UpdateDataModel

# TODO: Einlesen und Formatierung von Dateien aus dem Ordner "data"
# TODO: Markierung, sodass Dateien nicht doppelt gelesen werden
# TODO: Wie gehen wir mit beschädigten oder fehlerhaften Dateien um?
# TODO: Welche Daten sind interessant für uns?
# TODO: Wie finden wir heraus, ob bereits Sensordaten existieren?
# TODO: Wie senden wir Dateien an die Verwaltung?
# TODO: ...

class Bodenstation(object):
    def __init__(self,path: str):
        self.path = path

    def work(self):
        x = self.read()
        self.check(x[0],x[1])

    def read(self):
        path = self.path + 'TM_2024-07-30T13:43:41.893367.json'
        data = open(path, 'r', encoding='utf-8')
        data = json.load(data)
        #os.remove(path)
        return [data,path]

    def check(self,data,path):
        l = []
        for nils in data:
            l.append(nils)
        l2 = []
        for nils in l:
            l2.append(data[nils])
        if None in l2:
            return False




b = Bodenstation('data/')
b.read()



if __name__ == '__main__++++':
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