#!/usr/bin/env python
# coding=utf8
from __future__ import print_function, unicode_literals
from gi.repository import Gtk, Gdk, WebKit
import sys
import multiprocessing
from flask import Flask, request, render_template
import socket


try:
    from urllib2 import urlopen, HTTPError, URLError
except:
    from urllib.request import urlopen
    from urllib.error import HTTPError, URLError


class App(Gtk.Application):
    """App
    Application class
    """

    def __init__(self, module=None, host=None, port=None):
        Gtk.Application.__init__(self)
        self.flask = Flask(module)
        self.route = self.flask.route
        self.debug = False

        if port is None:
            """Port lock to be used by server later
            Don't forget to `self.socket.close()`
            """
            sock = socket.socket()
            sock.bind(('localhost', 0))
            self.port = sock.getsockname()[1]
            sock.close()

        self.host = host

    def do_startup(self):
        """Gtk.Application.run() will call this function()"""

        Gtk.Application.do_startup(self)
        gtk_window = Gtk.ApplicationWindow(application=self)
        gtk_window.set_title('AppKit')
        webkit_web_view = WebKit.WebView()
        webkit_web_view.load_uri('http://localhost:' + str(self.port))

        screen = Gdk.Screen.get_default()
        monitor_geometry = screen.get_primary_monitor()
        monitor_geometry = screen.get_monitor_geometry(monitor_geometry)

        settings = webkit_web_view.get_settings()
        settings.set_property('enable-universal-access-from-file-uris', True)
        settings.set_property('enable-file-access-from-file-uris', True)
        settings.set_property('default-encoding', 'utf-8')
        gtk_window.set_default_size(
            monitor_geometry.width * 1.0 / 2.0,
            monitor_geometry.height * 3.0 / 5.0,
        )
        scrollWindow = Gtk.ScrolledWindow()
        scrollWindow.add(webkit_web_view)
        gtk_window.add(scrollWindow)
        gtk_window.connect('delete-event', self._on_gtk_window_destroy)
        webkit_web_view.connect('notify::title', self._on_notify_title)
        self.gtk_window = gtk_window
        self.webkit_web_view = webkit_web_view
        gtk_window.show_all()

    def do_activate(self):
        """Gtk.Application.run() will call this function()
        after do_startup()
        """
        pass

    def _on_gtk_window_destroy(self, window, *args, **kwargs):
        self.server_process.terminate()

    def _on_notify_title(
            self,
            webkit_web_view,
            g_param_string,
            *args, **kwargs):
        title = webkit_web_view.get_title()
        if title is not None:
            self.gtk_window.set_title(title)

    def _run_server(self, port=None):
        self.flask.debug = self.debug
        process = multiprocessing.Process(
            target=self.flask.run,
            args=(self.host, self.port, self.debug),
            kwargs={
                'use_reloader': False,
            },
        )
        process.start()
        return process

    def _check_server(self):
        port = str(self.port)

        # These code may be replaced by using signal between
        # http server and GIO network
        while True:
            try:
                urlopen('http://localhost:' + port)
                break
            except HTTPError as e:
                print(e)
                break
            except URLError as e:
                pass

    def run(self, *args, **kw):
        self.server_process = self._run_server(
            port=self.port,
        )
        self._check_server()
        exit_status = super(App, self).run(sys.argv)
        sys.exit(exit_status)
