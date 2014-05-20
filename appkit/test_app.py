from appkit.app import *
import os
import unittest


class AppKitUnitTest(unittest.TestCase):
    def setUp(self):
        app = App(__name__)

        @app.route('/')
        def index():
            return '''
                <html>
                <head><title>Test App</title></head>
                <body>
                    Hello
                </body>
                <html>
            '''

        @app.route('/hi/')
        def hi():
            return 'hi'

        @app.route('/sum/<arg1>/<arg2>/')
        def sum(arg1, arg2):
            return int(arg1) + int(arg2)

        self.app = app


if __name__ == '__main__':
    unittest.main()
