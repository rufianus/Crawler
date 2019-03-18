# pip install kivy
# python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew

from kivy.app import App
from kivy.uix.widget import Widget

class PongGame(Widget):
    pass

class PongApp(App):
    def build(self):
        return PongGame()

if __name__ == '__main__':
    PongApp().run()

class PongGame2():

    def __init__(self):

        from kivy.app import App