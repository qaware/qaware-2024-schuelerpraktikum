import json
import pygame as py
import requests
from models import Sensor_data, UpdateDataModel

from BenutzerData import *
# TODO: Wie erhalten wir für uns interessante Informationen von der Verwaltung?
# TODO: Was sind interessante Daten und welche benötigen wir unter Umständen gar nicht?
# TODO: Wie gehen wir mit beschädigten bzw. falschen Informationen um?
# TODO: Wie stellen wir die Informationen bestmöglich für den Nutzer da?

class Animation(object):
    def __init__(self,display,colors):
        self.display = display
        self.colors = colors

    def sensorKnotrollscreen_Start(self, fenster,anzahlTypen):
        anzahlTypen = 1

        #statische Objekte werden gezeichnet
        fenster.fill(self.colors.black)
        # dynamischer Hintergrund für die Sensorentypen
        for x in range(anzahlTypen):
            py.draw.rect(fenster,self.colors.white,[self.display.getScreenWidth()*0.05,self.display.getScreenHeight()*0.05+self.display.getScreenHeight()*(0.95/anzahlTypen)*x, self.display.getScreenWidth()//6.67,self.display.getScreenHeight()*(0.85/anzahlTypen)],border_radius=10)

        #Hintergrund für die Diagramme
        py.draw.rect(fenster, self.colors.white, [self.display.getScreenWidth()*0.22, self.display.getScreenHeight()*0.05,self.display.getScreenWidth()*0.35, (self.display.getScreenHeight()*0.61)], border_radius=10)
        py.draw.rect(fenster, self.colors.white, [self.display.getScreenWidth()*0.6, self.display.getScreenHeight()*0.35,self.display.getScreenWidth()*0.35, (self.display.getScreenHeight()*0.61)], border_radius=10)

    def sensorKontrollScreen_Start_dynamisch(self,data):
        fenster = py.display.set_mode((self.display.getScreenWidth(),self.display.getScreenHeight()))
        py.display.set_caption("Satellitenkontrollprogramm")
        clock = py.time.Clock()
        data_typen = getAnzahlTypenausDaten(data)
        self.sensorKnotrollscreen_Start(fenster,len(data_typen))
        while True:
            for event in py.event.get():
                # Beenden bei [ESC] oder [X]
                if event.type == py.QUIT or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
                    py.quit()

            #display aktualisieren
            py.display.flip()
            clock.tick(self.display.getFPS())

def datenopen():
    for x in open("Example_data.json","r"):
        print(x)

def getAnzahlTypenausDaten(data):
    data_typen = []
    for messung in data:
        if data[messung]["type"] not in data_typen:
            data_typen += [data[messung]["type"]]
    return data_typen

if __name__ == '__main__':
    data = {"data": {"type": "thruster", "name": "thruster_3.c", "val": 8.703344683253974, "time": 215.2221422943402},"data2":{"type": "thruster", "name": "thruster_3.c", "val": 8.703344683253974, "time": 215.2221422943402}}
    screen = Screen()
    colors = Colors()
    animation = Animation(screen,colors)
    animation.sensorKontrollScreen_Start_dynamisch(data)
