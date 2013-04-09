#!/usr/bin/env python
# coding=utf8
from gi.repository import Gtk, Gdk, WebKit
import sys
import os
import multiprocessing
from flask import Flask
import socket
import urllib2

Gtk.init('')


class App(object):
    """App
    Application class
    """

    def __init__(self, module=None):
        self.server = Flask(module)
        self.route = self.server.route
        self.root_dir = os.path.abspath(
            os.path.dirname(module)
        )
        (self.gtk_window, self.webkit_web_view) = self._init_ui()

    def _init_ui(self):
        gtk_window = Gtk.Window()
        gtk_window.set_title('AppKit')
        webkit_web_view = WebKit.WebView()
        screen = Gdk.Screen.get_default()
        zoom_level = screen.get_height() / 900.0
        webkit_web_view.set_zoom_level(zoom_level)
        settings = webkit_web_view.get_settings()
        settings.set_property('enable-universal-access-from-file-uris', True)
        settings.set_property('enable-file-access-from-file-uris', True)
        settings.set_property('default-encoding', 'utf-8')
        gtk_window.set_default_size(800, 600)
        scrollWindow = Gtk.ScrolledWindow()
        scrollWindow.add(webkit_web_view)
        gtk_window.add(scrollWindow)
        gtk_window.connect('destroy', self._on_gtk_window_destroy)
        gtk_window.show_all()
        webkit_web_view.connect('notify::title', self._on_notify_title)
        return (gtk_window, webkit_web_view)

    def _on_gtk_window_destroy(self, window, *args, **kwargs):
        self.server_process.terminate()
        Gtk.main_quit()

    def _on_notify_title(
            self,
            webkit_web_view,
            g_param_string,
            *args, **kwargs):
        print 'on_notify_title'
        title = webkit_web_view.get_title()
        if title is not None:
            self.gtk_window.set_title(title)

    def _run_server(self, publish=False, port=None, debug=False):
        if port is None:
            sock = socket.socket()
            sock.bind(('localhost', 0))
            port = sock.getsockname()[1]
            sock.close()

        if publish:
            host = '0.0.0.0'
        else:
            host = 'localhost'

        process = multiprocessing.Process(
            target=self.server.run,
            args=(host, port, debug),
            kwargs={'use_reloader': False},
        )
        process.start()
        return (process, port)

    def _check_server(self, port=None):
        port = str(port)
        while True:
            try:
                urllib2.urlopen('http://localhost:' + port)
                break
            except urllib2.HTTPError as e:
                print e
                break
            except urllib2.URLError as e:
                pass

    def run(self, publish=False, port=None, debug=False):
        (self.server_process, self.port) = self._run_server(
            publish=publish,
            port=port,
            debug=debug
        )
        self._check_server(port=self.port)
        self.webkit_web_view.load_uri('http://localhost:' + str(self.port))
        sys.exit(Gtk.main())
