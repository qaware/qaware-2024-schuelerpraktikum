import json
import os
import requests

from models import SensorData, UpdateDataModel

class Bodenstation(object):
    def __init__(self,path: str):
        self.path = path
        self.fehlerspeicher = {'thruster_1.a': [],
                               'thruster_1.b': [],
                               'oxygen_tank_1': [],
                               'oxygen_tank_2': [],
                               'unkown': []}


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
        l2 = []
        for nils in ak_data:
            l.append(nils)
            l2.append(ak_data[nils])
        #if (not 'type' in l or not 'value' in l) and 'name' in l and 'time' in l:
        #    print('Datei fehlerhaft')
        #    if not ak_data['name'] == None and not ak_data['time'] == None:
        #        self.recycle(ak_data)
        #    else:
        #        pass
        #    return False
        if None in l2:
            print('Datei fehlerhaft')
            self.recycle(ak_data)
            return False
        answer = requests.get(f"http://127.0.0.1:8000/data/doesExist/{ak_data['data_type']}/{ak_data['name']}/{ak_data['time']}")
        if answer.content == False:
            print('Daten bereits vorhanden')
            return False
        data_obj = SensorData(name=ak_data['name'],time=ak_data['time'],data_type=ak_data['data_type'],value=ak_data['value'])
        x = requests.post(f"http://127.0.0.1:8000/data/addData",data_obj.json())
        print(x.content)
        return x.content

    def recycle(self,ak_data):
        pruef = []
        if not ak_data['time'] == None and not ak_data['name'] == False:
            try:
                self.fehlerspeicher[ak_data['name']].append(ak_data['time'])
            except:
                self.fehlerspeicher[ak_data['name']] = []
                self.fehlerspeicher[ak_data['name']].append(ak_data['time'])
            pruef = [ak_data['name'],ak_data['time']]
        elif not ak_data['name'] == None:
            try:
                self.fehlerspeicher[ak_data['name']].append('unkown')
            except:
                self.fehlerspeicher[ak_data['name']] = []
                self.fehlerspeicher[ak_data['name']].append('unkown')

        elif not ak_data['time'] == None:
            self.fehlerspeicher['unkown'].append(ak_data['time'])
            pruef = ['unkown',ak_data['time']]
        else:
            self.fehlerspeicher['unkown'].append('unkown')
        if len(pruef) > 0:
            l = self.fehlerspeicher[pruef[0]]
            if len(l) >= 3:
                dif = (l[0]-l[1])+(l[1]-l[2])
                if dif <= 8:
                    print('Warning! Sensor ' + str(pruef[0]) + 'hat wahrscheinlich eine Funktionsstörung!')

    def auslesen(self):
        print('Fehlerspeicher Auslese:')
        for nils in self.fehlerspeicher:
            print(nils + ': ' + str(len(self.fehlerspeicher[nils])) + ' Fehler gespeichert')
        print('Genauere Informationen zum zeitlichen Auftreten der Fehler:')
        for nils in self.fehlerspeicher:
            print(nils + ': ' + str(self.fehlerspeicher[nils]))




b = Bodenstation('data/')
b.work()
b.auslesen()