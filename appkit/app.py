#!/usr/bin/env python
from gi.repository import Gtk, WebKit
from urlparse import urlparse, parse_qs
import os
import tempfile
import mimetypes
import codecs
import sys

Gtk.init('')


class App(object):
    """App
    Application class
    """
    registed_route = dict()  # for url to function mapping
    document = None  # Root DOM

    def __init__(self, app_path=None):
        app_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        window = Gtk.Window()
        window.set_title('AppKit')
        webkit_web_view = WebKit.WebView()
        settings = webkit_web_view.get_settings()
        settings.set_property('enable-universal-access-from-file-uris', True)
        settings.set_property('enable-developer-extras', True)
        settings.set_property('default-encoding', 'utf-8')
        window.set_default_size(800, 600)
        scrollWindow = Gtk.ScrolledWindow()
        scrollWindow.add(webkit_web_view)
        window.add(scrollWindow)
        window.connect('destroy', Gtk.main_quit)
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
            self.on_resource_load_finished)
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
        window.show_all()
        self.window = window
        self.webkit_web_view = webkit_web_view
        self.webkit_main_frame = webkit_main_frame
        self.app_path = app_path

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

    def on_web_view_resource_request_starting(
            self,
            web_view,
            web_frame,
            web_resource,
            network_request,
            network_response=None):
        print 'web_view_resource_request_starting'

    def on_web_view_resource_response_received(
            self,
            web_view,
            web_frame,
            web_resource,
            network_response,
            *arg, **kw):
        print 'web_view Resource response received'

    def on_web_frame_resource_request_starting(
            self,
            web_frame,
            web_resource,
            network_request,
            network_response=None):
        print 'web_frame_resource_request_starting'
        url = urlparse(network_request.get_uri())
        if url.scheme == 'app':
            if url.netloc == '':
                result = self.registed_route[url.path]()
                # Make sure result is <tuple>
                if isinstance(result, str):
                    result = (result,)
                (content, mimetype, encoding) = response(*result)
                file_ext = mimetypes.guess_extension(mimetype)
                tmp_file_path = tempfile.mkstemp(suffix=file_ext)[1]
                f = codecs.open(tmp_file_path, 'w', encoding)
                f.write(content)
                f.close()
                network_request.set_uri('file://' + tmp_file_path + '?tmp=1')
            elif url.netloc == 'file':
                file_path = self.app_path + url.path
                file_path = os.path.normcase(file_path)
                network_request.set_uri('file://' + file_path)

    def on_web_frame_resource_response_received(
            self,
            web_frame,
            web_resource,
            network_response,
            *arg, **kw):
        print 'web_frame Resource response received'
        url = urlparse(network_response.get_uri())
        url = urlparse(url.path)
        query = parse_qs(url.query)
        if 'tmp' in query:
            print url.path
            os.remove(url.path)

    def on_resource_load_finished(
            self,
            web_view, web_frame, web_resource,
            *args, **kw):
        print 'resource load finished'

    def run(self):
        self.webkit_web_view.load_uri('app:///')
        Gtk.main()

    def _get_app_path(self, path='.'):
        print self.__file__

    def request_handler():
        pass


def response(content=None, mimetype='text/html', encoding='utf-8'):
    return (content, mimetype, encoding)
