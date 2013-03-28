#!/usr/bin/env python
# coding=utf8
from gi.repository import Gtk, WebKit
import sys
from multiprocessing import Process
from flask import Flask
import socket
import urllib2

Gtk.init('')


class UI(object):
    def __init__(self, debug=False):
        self.debug = debug
        gtk_window = Gtk.Window()
        gtk_window.set_title('AppKit')
        webkit_web_view = WebKit.WebView()
        settings = webkit_web_view.get_settings()
        settings.set_property('enable-universal-access-from-file-uris', True)
        settings.set_property('enable-file-access-from-file-uris', True)
        settings.set_property('default-encoding', 'utf-8')
        gtk_window.set_default_size(800, 600)
        scrollWindow = Gtk.ScrolledWindow()
        scrollWindow.add(webkit_web_view)
        gtk_window.add(scrollWindow)
        gtk_window.connect('destroy', Gtk.main_quit)
        webkit_web_view.connect(
            'notify::load-status',
            self.on_notify_load_status)
        webkit_web_view.connect(
            'resource-request-starting',
            self.on_web_view_resource_request_starting)
        webkit_web_view.connect(
            'resource-response-received',
            self.on_web_view_resource_response_received)
        webkit_web_view.connect(
            'resource-load-finished',
            self.on_web_view_resource_load_finished)
        webkit_web_view.connect(
            'navigation_policy_decision_requested',
            self.on_navigation_policy_decision_requested)

        webkit_main_frame = webkit_web_view.get_main_frame()
        webkit_main_frame.connect(
            'resource-request-starting',
            self.on_web_frame_resource_request_starting)
        webkit_main_frame.connect(
            'resource-response-received',
            self.on_web_frame_resource_response_received)
        webkit_main_frame.connect(
            'resource-load-finished',
            self.on_web_frame_resource_load_finished)
        webkit_main_frame.connect(
            'resource-load-failed',
            self.on_web_frame_resource_load_failed)

        gtk_window.show_all()
        self.gtk_window = gtk_window
        self.webkit_web_view = webkit_web_view
        self.webkit_main_frame = webkit_main_frame

    def on_notify_load_status(self, webkitView, *args, **kwargs):
        """Callback function when the page was loaded completely
        FYI, this function will be called after $(document).ready()
        in jQuery
        """
        status = webkitView.get_load_status()
        if status == status.FINISHED:
            if self.debug is True:
                print 'Load finished'

    def on_navigation_policy_decision_requested(
            self,
            webkit_web_view,
            webkit_web_frame,
            webkit_network_request,
            webkit_web_navigation_action,
            webkit_web_policy_dicision):
        if self.debug is True:
            print 'on_navigation_policy_decision_requested'

    def on_web_view_resource_request_starting(
            self,
            web_view,
            web_frame,
            web_resource,
            network_request,
            network_response=None):
        if self.debug is True:
            print network_request.get_uri()
            print 'on_web_view_resource_request_starting'

    def on_web_view_resource_response_received(
            self,
            web_view,
            web_frame,
            web_resource,
            network_response,
            *arg, **kw):
        if self.debug is True:
            print 'on_web_view_resource_response_received'

    def on_web_view_resource_load_finished(
            self,
            web_view, web_frame, web_resource,
            *args, **kw):
        if self.debug is True:
            print 'on_web_view_resource_load_finished'

    def on_web_frame_resource_request_starting(
            self,
            web_frame,
            web_resource,
            network_request,
            network_response=None):
        if self.debug is True:
            print 'on_web_frame_resource_request_starting'

    def on_web_frame_resource_response_received(
            self,
            web_frame,
            web_resource,
            network_response,
            *arg, **kw):
        if self.debug is True:
            print 'on_web_frame_resource_response_received'

    def on_web_frame_resource_load_finished(
            self,
            web_frame,
            web_resource,
            *arg, **kw):
        if self.debug is True:
            print 'on_web_frame_resource_load_finished'

    def on_web_frame_resource_load_failed(
            self,
            web_frame,
            web_resource,
            *arg, **kw):
        if self.debug is True:
            print 'on_web_frame_resource_load_failed'


class App(object):
    """App
    Application class
    """

    def __init__(self, module_name=None):
        self.ui = UI()
        self.server = Flask(module_name)

    def run(self):
        # Start web server
        sock = socket.socket()
        sock.bind(('localhost', 0))
        port = sock.getsockname()[1]
        sock.close()
        self.port = str(port)
        p = Process(
            target=self.server.run,
            args=('localhost', port,),
        )
        p.daemon = True
        p.start()
        while True:
            try:
                urllib2.urlopen('http://localhost:' + self.port)
                break
            except:
                pass

        self.ui.webkit_web_view.load_uri('http://localhost:' + self.port)
        sys.exit(Gtk.main())
