import json
import os
import requests

from models import SensorData, UpdateDataModel

class Bodenstation(object):
    def __init__(self,path: str):
        self.path = path

    def work(self):
        x = self.read()
        self.check(x[0],x[1])

    def read(self):
        all_data = []
        for nils in os.listdir('data'):
            all_data.append(nils)
        path = self.path + all_data[0]
        ak_data = open(path, 'r', encoding='utf-8')
        ak_data = json.load(ak_data)
        os.remove(path)
        return [ak_data,path]

    def check(self,ak_data,path):
        l = []
        for nils in ak_data:
            l.append(nils)
        l2 = []
        for nils in l:
            l2.append(ak_data[nils])
        if None in l2:
            return False
        answer = requests.get(f"http://127.0.0.1:8000/data/doesExist/{ak_data['data_type']}/{ak_data['name']}/{ak_data['time']}")
        if answer.content == False:
            return False
        data_obj = SensorData(name=ak_data['name'],time=ak_data['time'],data_type=ak_data['data_type'],value=ak_data['value'])
        requests.post(f"htp://127.0.0.1:8000/data/addData",data_obj.json())