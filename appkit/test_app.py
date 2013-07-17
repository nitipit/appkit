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

    def test_init_gtk(self):
        try:
            Gtk.init('')
        except:
            raise Exception('Can\'t init Gtk')

    def test___init__(self):
        self.assertIsInstance(self.app.gtk_window, Gtk.Window)
        self.assertIsInstance(self.app.webkit_web_view, WebKit.WebView)
        self.assertTrue(os.path.isdir(self.app.root_dir))

    def test__init_ui(self):
        self.app._init_ui()
        self.assertEqual(self.app.gtk_window.get_title(), 'AppKit')

    def test__run_server(self):
        (process, port) = self.app._run_server()
        print(process)
        self.assertIsInstance(process, multiprocessing.Process)
        self.assertIsInstance(port, int)
        process.terminate()


if __name__ == '__main__':
    unittest.main()
