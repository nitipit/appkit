#!/usr/bin/env python

from appkit.api.v0_2_4.app import *
import os
import unittest


class AppKitUnitTest(unittest.TestCase):
    def setUp(self):
        app = App(__file__)

        @app.route('^/$')
        def index():
            return '''
                <html>
                <head><title>Test App</tible></head>
                <body>
                    Hello
                </body>
                <html>
            '''

        @app.route('/hi')
        def hi():
            return 'hi'

        @app.route('/sum/(.+)/(.+)/')
        def sum(arg1, arg2):
            return int(arg1) + int(arg2)

        self.app = app

    def test_init_gtk(self):
        try:
            Gtk.init('')
        except:
            raise Exception('Can\'t init Gtk')

    def test___init__(self):
        self.assertIsInstance(self.app.window, Gtk.Window)
        self.assertIsInstance(self.app.webkit_web_view, WebKit.WebView)
        self.assertIsInstance(self.app.webkit_main_frame, WebKit.WebFrame)
        self.assertTrue(os.path.isdir(self.app.app_dir))

    def test_route(self):
        self.assertEqual(self.app.url_pattern.keys()[0], '^/$')
        self.assertTrue(hasattr(self.app.url_pattern['^/$'], '__call__'))

    def test__url_map_to_function(self):
        self.assertEqual(self.app._url_map_to_function('/hi'), 'hi')
        self.assertEqual(self.app._url_map_to_function('/sum/1/2/'), 3)

    def test__init_ui(self):
        self.app._init_ui()
        self.assertEqual(self.app.window.get_title(), 'Test App')

if __name__ == '__main__':
    unittest.main()
