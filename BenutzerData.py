import pygame as py

class Screen(object):
    def __init__(self):
        self.screen_width = 1500
        self.screen_height = 820
        self.fps = 60

    def getScreenHeight(self):
        return self.screen_height

    def getScreenWidth(self):
        return self.screen_width

    def getFPS(self):
        return self.fps

class Colors(object):
    def __init__(self):
        #Die Farben werden definiert
        self.grey = (112, 128, 144)
        self.light_grey = (165, 175, 185)
        self.blackish = (10, 10, 10)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.gold = (215,175,55)
        self.grey_brown = (63,58,58)
        self.green_normal = (45,175,20)
        self.light_green = (0, 255, 0)
        self.blue = (0,29,200)
        self.blue_light = (0,5,255)
        self.grey_dark = (34,34,34)
        self.brown = (23,17,9)
        self.aqua = (0,255,255)
        self.sand = (235, 160, 45)
        self.sand_light = (255, 190, 75)
        self.red = (255,0,0)
        self.dark_red = (200, 0, 0)
        self.silver = (120,120,120)
        self.colorPlatten = [[self.black, self.grey, self.light_grey, self.grey_dark, self.silver,(128,128,128)],
                             [self.green_normal, self.light_green, (0,51,0),(0,102,0),(0,255,0),(0,153,73)],
                             [self.gold, self.sand, self.sand_light,(255,255,0),(102,102,0),(255,255,102)],
                             [self.dark_red, self.red]]


class Fonts(object):
    def __init__(self):
        self.large_font = py.font.SysFont("comicsansms", 130)
        self.medium_font = py.font.SysFont("comicsansms", 110, "bold")
        self.large2_font = py.font.SysFont("comicsansms", 80, "bold")
        self.font = py.font.SysFont("comicsansms", 42)
        self.small_font = py.font.SysFont("comicsansms", 25)