#!/usr/bin/env python
from gi.repository import Gtk, WebKit
from urlparse import urlparse
import os

Gtk.init('')


class App(object):
    """App
    Application class
    """
    registed_route = dict()  # for url to function mapping
    document = None  # Root DOM

    def __init__(self):
        base_path = os.path.abspath(os.path.dirname(__file__))
        window = Gtk.Window()
        window.set_title('AppKit')
        webkit_web_view = WebKit.WebView()
        settings = webkit_web_view.get_settings()
        settings.set_property('enable-universal-access-from-file-uris', True)
        settings.set_property('enable-developer-extras', True)
        window.set_default_size(800, 600)
        scrollWindow = Gtk.ScrolledWindow()
        scrollWindow.add(webkit_web_view)
        window.add(scrollWindow)
        window.connect('destroy', Gtk.main_quit)
        webkit_web_view.connect('notify::load-status', self.on_notify_load_status)
        webkit_web_view.connect('resource-request-starting', self.on_resource_request_starting)
        webkit_web_view.connect('resource-load-finished', self.on_resource_load_finished)
        webkit_web_view.connect(
            'navigation_policy_decision_requested',
            self.on_navigation_policy_decision_requested)
        window.show_all()
        self.window = window
        self.webkit_web_view = webkit_web_view
        self.base_path = base_path

    def route(self, path=None):
        def decorator(fn):
            self.registed_route[path] = fn
            return fn
        return decorator

    def on_notify_load_status(self, webkitView, *args, **kwargs):
        """Callback function when the page was loaded completely
        FYI, this function will be called after $(document).ready()
        in jQuery
        """
        status = webkitView.get_load_status()
        if status == status.FINISHED:
            print 'Load finished'

    def on_navigation_policy_decision_requested(
            self,
            webkit_web_view,
            webkit_web_frame,
            webkit_network_request,
            webkit_web_navigation_action,
            webkit_web_policy_dicision):
        print 'navigation_policy_decision_requested'
        url = urlparse(webkit_network_request.get_uri())
        print url
        if url[0] != 'app':
            return False
        # TODO: need more improvement about path mapping
        # Will look for some idea from Python web framework
        # Such as `Flask`, `CherryPy`
        path = url.path.split('/')
        for i in range(path.count('')):
            path.remove('')

        for key in self.registed_route.keys():
            route = key.split('/')
            for i in range(route.count('')):
                route.remove('')
            if path == route:
                print 'Route found'
                self.registed_route[key](self)
                return True

    def on_resource_request_starting(
            self,
            webkit_web_view,
            webkit_web_frame,
            webkit_web_resource,
            webkit_web_request,
            webkit_web_response):
        print 'Resource request starting'

    def on_resource_load_finished(
            self,
            webkit_web_view, webkit_web_frame, webkit_web_resource,
            *args, **kw):
        print 'resource load finished'

    def run(self):
        self.webkit_web_view.load_uri('app:///')
        Gtk.main()
