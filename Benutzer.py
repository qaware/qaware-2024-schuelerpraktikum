import json

import pygame.display
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

    def startScreen(self):
        fenster = py.display.set_mode((self.display.getScreenWidth(),self.display.getScreenHeight()))
        py.display.set_caption("Satellitenkontrollprogramm")
        clock = py.time.Clock()

        #statische Objekte
        fenster.fill(self.colors.black)
        py.draw.rect(fenster,self.colors.white,[self.display.getScreenWidth()//20,self.display.getScreenHeight()//20, self.display.getScreenWidth()//6.67,self.display.getScreenHeight()//2.23],border_radius=10)
        py.draw.rect(fenster,self.colors.white,[self.display.getScreenWidth()//20,self.display.getScreenHeight()//1.82, self.display.getScreenWidth()//6.67,self.display.getScreenHeight()-self.display.getScreenHeight()//20],border_radius=10)

        while True:
            for event in py.event.get():
                # Beenden bei [ESC] oder [X]
                if event.type == py.QUIT or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
                    py.quit()

            #display aktualisieren
            py.display.flip()
            clock.tick(self.display.getFPS())

if __name__ == '__main__':
    #data = Sensor_data(name="Test")
    py.init()
    screen = Screen()
    colors = Colors()
    animation = Animation(screen,colors)
    animation.startScreen()
    """new_data = UpdateDataModel(name="Updated Test")
    answer1 = requests.post("http://127.0.0.1:8000/data/", data.json())
    answer2 = requests.put(f"http://127.0.0.1:8000/data/{json.loads(answer1.content)['_id']}", new_data.json())
    answer3 = requests.delete(f"http://127.0.0.1:8000/data/{json.loads(answer1.content)['_id']}")
    answer4 = requests.get(f"http://127.0.0.1:8000/data/{json.loads(answer1.content)['_id']}")
    print(answer1.content)
    print(answer2.content)
    print(answer3.content)
    print(answer4.content)"""
