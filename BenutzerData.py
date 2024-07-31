class Screen(object):
    def __init__(self):
        self.screen_width = 1300
        self.screen_height = 700
        self.fps = 60

    def getScreenHeight(self):
        return self.screen_height

    def getScreenWidth(self):
        return self.screen_width

    def getFPS(self):
        return self.fps

class Colors(object):
    def __init__(self):
        self.black = (0,0,0)
        self.white = (255,255,255)