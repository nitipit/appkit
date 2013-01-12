from appkit.app import App
import os


class App(App):
    def __init__(self, module_path=None):
        app_path = os.path.abspath(os.path.dirname(module_path))
        super(App, self).__init__(app_path=app_path)
