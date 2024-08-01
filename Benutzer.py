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
    def __init__(self, display, colors, fonts):
        self.display = display
        self.colors = colors
        self.fonts = fonts

    def sensorKnotrollscreen_Start(self, fenster,data_typen):
        # statische Objekte werden gezeichnet
        fenster.blit(py.image.load(os.path.join('images', 'space.jpg')),(0,0))
        # dynamischer Hintergrund für die Sensorentypen
        for x in range(len(data_typen)):
            py.draw.rect(fenster,self.colors.white,[self.display.getScreenWidth()*0.05,self.display.getScreenHeight()*0.05+self.display.getScreenHeight()*(0.95/len(data_typen))*x, self.display.getScreenWidth()//6.67,self.display.getScreenHeight()*(0.85/len(data_typen))],border_radius=10)

        # Hintergrund für die Diagramme
        py.draw.rect(fenster, self.colors.white, [self.display.getScreenWidth()*0.22, self.display.getScreenHeight()*0.05,self.display.getScreenWidth()*0.35, (self.display.getScreenHeight()*0.61)], border_radius=10)
        py.draw.rect(fenster, self.colors.white, [self.display.getScreenWidth()*0.6, self.display.getScreenHeight()*0.35,self.display.getScreenWidth()*0.35, (self.display.getScreenHeight()*0.61)], border_radius=10)

        # die x und y Achsen

        # Diagramm links
        py.draw.line(fenster,self.colors.black,(self.display.getScreenWidth()*0.24,self.display.getScreenHeight()*0.07),(self.display.getScreenWidth()*0.24,self.display.getScreenHeight()*0.62))
        py.draw.line(fenster,self.colors.black,(self.display.getScreenWidth()*0.24,self.display.getScreenHeight()*0.62),(self.display.getScreenWidth()*0.56,self.display.getScreenHeight()*0.62))
        # Diagramm rechts
        py.draw.line(fenster,self.colors.black,(self.display.getScreenWidth()*0.62,self.display.getScreenHeight()*0.37),(self.display.getScreenWidth()*0.62,self.display.getScreenHeight()*0.92))
        py.draw.line(fenster,self.colors.black,(self.display.getScreenWidth()*0.62,self.display.getScreenHeight()*0.92),(self.display.getScreenWidth()*0.93,self.display.getScreenHeight()*0.92))

        self.addHeadlines(data_typen,fenster)
        self.addNamen(data,fenster)
        self.drawDiagramm(getMessdatenvonSensor(data),fenster,self.display.getScreenWidth()*0.62,self.display.getScreenHeight()*0.37)

    def sensorKontrollScreen_Start_dynamisch(self,data):
        fenster = py.display.set_mode((self.display.getScreenWidth(),self.display.getScreenHeight()))
        py.display.set_caption("Satellitenkontrollprogramm")
        clock = py.time.Clock()
        data_typen = getTypenausDaten(data)
        self.sensorKnotrollscreen_Start(fenster,data_typen)
        while True:
            for event in py.event.get():
                # TODO schließen des Programms bei Betätigung von X
                # Beenden bei [ESC] oder [X]
                if event.type == py.QUIT or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
                    py.quit()

            # Display aktualisieren
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

    def drawDiagramm(self,messdaten,fenster, x_start_pixel, y_start_pixel):
        minMaxData,min,max = getMinundMaxfromData(messdaten)
        print(minMaxData)
        pixelWidth = self.display.getScreenWidth()*0.33
        pixelHeight = self.display.getScreenHeight()*0.55
        if max-min != 0:
            faktorHeight = pixelHeight/(max-min)
        else:
            faktorHeight = 2
        for messung in minMaxData:
            print("Pixelwidth", pixelWidth)
            faktorWidth = pixelWidth/minMaxData[messung]["anzahl"]
            print("-----",faktorWidth,faktorHeight,minMaxData[messung]["anzahl"])
            for value_index in range(len(messdaten[messung])-1):
                py.draw.line(fenster,self.colors.black, (x_start_pixel+faktorWidth*value_index, y_start_pixel+faktorHeight*(messdaten[messung][value_index]-min)),(x_start_pixel+faktorWidth*(value_index+1),y_start_pixel+faktorHeight*(messdaten[messung][value_index+1]-min)))
                print(x_start_pixel+faktorWidth*value_index,":", y_start_pixel+faktorHeight*(messdaten[messung][value_index]-min),":",x_start_pixel+pixelWidth*(value_index+1), ":", y_start_pixel+faktorHeight*(messdaten[messung][value_index+1]-min))
            break

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
        elif data[messung]["name"] not in sensoren_namen[data[messung]["data_type"]]:
            sensoren_namen[data[messung]["data_type"]] += [data[messung]["name"]]
    return sensoren_namen

def getMessdatenvonSensor(data,name=0):
    messdaten = {}
    for messung in data:
        if name == 0:
            if data[messung]["name"] not in messdaten.keys():
                messdaten[data[messung]["name"]] = [data[messung]["val"]]
            else:
                messdaten[data[messung]["name"]] += [data[messung]["val"]]
        else:
            if messung == name and data[messung] not in messdaten.keys():
                messdaten[data[messung]["name"]] = [data[messung]["val"]]
            else:
                messdaten[data[messung]["name"]] += [data[messung]["val"]]
    return messdaten

def getMinundMaxfromData(messdaten):
    minMaxData = {}
    gesMin = float("inf")
    gesMax = 0
    for sensor in messdaten:
        min = float("inf")
        max = 0
        anzahlMessungen = 0
        for messdata in messdaten[sensor]:
            anzahlMessungen += 1
            if messdata > max:
                max = messdata
            if messdata < min:
                min = messdata
            if messdata > gesMax:
                gesMax = messdata
            if messdata < gesMin:
                gesMin = messdata
        minMaxData[sensor] = {"min": min, "max": max, "anzahl": anzahlMessungen}
    return minMaxData, gesMin, gesMax

if __name__ == '__main__':
    py.init()
    data = {"data": {"data_type": "thruster", "name": "thruster_3.c", "val": 8.703344683253974, "time": 215.2221422943402},"data2":{"data_type": "temperatur", "name": "temp1", "val": 18.703344683253974, "time": 215.2221422943402},"data3":{"data_type": "temperatur", "name": "temp2", "val": 2.703344683253974, "time": 215.2221422943402},
            "data1234": {"data_type": "thruster", "name": "thruster_3.c", "val": 28.703344683253974, "time": 215.2221422943402},"data32": {"data_type": "thruster", "name": "thruster_3.c", "val": 18.703344683253974, "time": 215.2221422943402},"data4": {"data_type": "thruster", "name": "thruster_3.c", "val": 58.703344683253974, "time": 215.2221422943402},
            "data234": {"data_type": "thruster", "name": "thruster_3.c", "val": 83.703344683253974, "time": 215.2221422943402},"data7": {"data_type": "thruster", "name": "thruster_3.c", "val": 8.344683253974, "time": 215.2221422943402},
            "data435": {"data_type": "thruster", "name": "thruster_3.c", "val": 148.703344683253974, "time": 215.2221422943402},"data45": {"data_type": "thruster", "name": "thruster_3.c", "val": 68.703344683253974, "time": 215.2221422943402},"data56": {"data_type": "thruster", "name": "temp1", "val": 100.703344683253974, "time": 215.2221422943402},
            "data3564657": {"data_type": "thruster", "name": "thruster_3.c", "val": 8.703344683253974, "time": 215.2221422943402},"data345": {"data_type": "thruster", "name": "temp2", "val": 38.703344683253974, "time": 215.2221422943402},"data977": {"data_type": "thruster", "name": "temp1", "val": 13.703344683253974, "time": 215.2221422943402}}
    print(getMinundMaxfromData(getMessdatenvonSensor(data)))
    screen = Screen()
    colors = Colors()
    fonts = Fonts()
    animation = Animation(screen,colors,fonts)
    animation.sensorKontrollScreen_Start_dynamisch(data)
