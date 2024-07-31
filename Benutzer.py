import json
import requests
import os
#from models import Sensor_data, UpdateDataModel

from BenutzerData import *
# TODO: Wie erhalten wir für uns interessante Informationen von der Verwaltung?
# TODO: Was sind interessante Daten und welche benötigen wir unter Umständen gar nicht?
# TODO: Wie gehen wir mit beschädigten bzw. falschen Informationen um?
# TODO: Wie stellen wir die Informationen bestmöglich für den Nutzer da?

class Animation(object):
    def __init__(self,display,colors,fonts):
        self.display = display
        self.colors = colors
        self.fonts = fonts

    def sensorKnotrollscreen_Start(self, fenster,data_typen):
        #statische Objekte werden gezeichnet
        fenster.blit(py.image.load(os.path.join('images', 'space.jpg')),(0,0))
        # dynamischer Hintergrund für die Sensorentypen
        for x in range(len(data_typen)):
            py.draw.rect(fenster,self.colors.white,[self.display.getScreenWidth()*0.05,self.display.getScreenHeight()*0.05+self.display.getScreenHeight()*(0.95/len(data_typen))*x, self.display.getScreenWidth()//6.67,self.display.getScreenHeight()*(0.85/len(data_typen))],border_radius=10)

        #Hintergrund für die Diagramme
        py.draw.rect(fenster, self.colors.white, [self.display.getScreenWidth()*0.22, self.display.getScreenHeight()*0.05,self.display.getScreenWidth()*0.35, (self.display.getScreenHeight()*0.61)], border_radius=10)
        py.draw.rect(fenster, self.colors.white, [self.display.getScreenWidth()*0.6, self.display.getScreenHeight()*0.35,self.display.getScreenWidth()*0.35, (self.display.getScreenHeight()*0.61)], border_radius=10)

        self.addHeadlines(data_typen,fenster)
        self.addNamen(data,fenster)

    def sensorKontrollScreen_Start_dynamisch(self,data):
        fenster = py.display.set_mode((self.display.getScreenWidth(),self.display.getScreenHeight()))
        py.display.set_caption("Satellitenkontrollprogramm")
        clock = py.time.Clock()
        data_typen = getTypenausDaten(data)
        self.sensorKnotrollscreen_Start(fenster,data_typen)
        while True:
            for event in py.event.get():
                # Beenden bei [ESC] oder [X]
                if event.type == py.QUIT or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
                    py.quit()

            #Display aktualisieren
            py.display.flip()
            clock.tick(self.display.getFPS())

    def addHeadlines(self,data_typen,fenster):
        fenster.blit(self.fonts.font.render("alle historische Daten", True, self.colors.light_grey), (self.display.getScreenWidth()*0.61,self.display.getScreenHeight()*0.25))
        fenster.blit(self.fonts.font.render("letzten Daten", True, self.colors.light_grey), (self.display.getScreenWidth()*0.23,self.display.getScreenHeight()*0.67))
        for index,sensorArt in enumerate(data_typen):
            fenster.blit(self.fonts.small_font.render(sensorArt, True, self.colors.blackish), (self.display.getScreenWidth()*0.07,self.display.getScreenHeight()*0.06+self.display.getScreenHeight()*(0.95/len(data_typen))*index))

    def addNamen(self,data,fenster):
        sensoren_namen = getSensorenNamen(data)
        for sensor_typ_index,sensorTyp in enumerate(sensoren_namen):
            for sensor_name_index,sensorName in enumerate(sensoren_namen[sensorTyp]):
                fenster.blit(self.fonts.small_font.render(sensorName, True, self.colors.light_grey), (self.display.getScreenWidth()*0.07,self.display.getScreenHeight()*0.11+self.display.getScreenHeight()*(0.95/len(sensoren_namen))*sensor_typ_index+35*sensor_name_index))

def datenopen():
    for x in open("Example_data.json","r"):
        print(x)

def getTypenausDaten(data):
    data_typen = []
    for messung in data:
        if data[messung]["data_type"] not in data_typen:
            data_typen += [data[messung]["data_type"]]
    return data_typen

def getSensorenNamen(data):
    sensoren_namen = {}
    for messung in data:
        if data[messung]["data_type"] not in sensoren_namen.keys():
            sensoren_namen[data[messung]["data_type"]] = [data[messung]["name"]]
        else:
            sensoren_namen[data[messung]["data_type"]] += [data[messung]["name"]]
    return sensoren_namen


if __name__ == '__main__':
    py.init()
    data = {"data": {"data_type": "thruster", "name": "thruster_3.c", "val": 8.703344683253974, "time": 215.2221422943402},"data2":{"data_type": "temperatur", "name": "thruster_3.c", "val": 8.703344683253974, "time": 215.2221422943402},"data3":{"data_type": "temperatur", "name": "thruster_3.c", "val": 8.703344683253974, "time": 215.2221422943402}}
    screen = Screen()
    colors = Colors()
    fonts = Fonts()
    animation = Animation(screen,colors,fonts)
    animation.sensorKontrollScreen_Start_dynamisch(data)
