#!/usr/bin/env python
# coding=utf8
from gi.repository import Gtk, Gdk, WebKit
import sys
import os
from multiprocessing import Process
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
        gtk_window.connect('destroy', Gtk.main_quit)
        gtk_window.show_all()
        webkit_web_view.connect('notify::title', self._on_notify_title)
        self.gtk_window = gtk_window
        self.webkit_web_view = webkit_web_view

    def _on_notify_title(
            self,
            webkit_web_view,
            g_param_string,
            *args, **kwargs):
        print 'on_notify_title'
        title = webkit_web_view.get_title()
        if title is not None:
            self.gtk_window.set_title(title)

    def _run_server(self):
        # Start web server
        sock = socket.socket()
        sock.bind(('localhost', 0))
        port = sock.getsockname()[1]
        sock.close()
        self.port = str(port)
        p = Process(
            target=self.server.run,
            args=('0.0.0.0', port,),
        )
        p.daemon = True
        p.start()
        while True:
            try:
                urllib2.urlopen('http://localhost:' + self.port)
                break
            except urllib2.HTTPError as e:
                print e
                break
            except urllib2.URLError as e:
                pass

    def run(self, debug=False):
        if debug:
            self.server.run(debug=debug)
        else:
            self._init_ui()
            self._run_server()
            self.webkit_web_view.load_uri('http://localhost:' + self.port)
            sys.exit(Gtk.main())
