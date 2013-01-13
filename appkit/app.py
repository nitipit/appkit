#!/usr/bin/env python
# coding=utf8
from gi.repository import Gtk, WebKit
import urlparse
import os
import tempfile
import mimetypes
import codecs
import sys
import re

Gtk.init('')


class App(object):
    """App
    Application class
    """
    url_pattern = dict()
    debug = False

    def __init__(self, app_path=None):
        if app_path is None:
            app_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        window = Gtk.Window()
        window.set_title('AppKit')
        webkit_web_view = WebKit.WebView()
        settings = webkit_web_view.get_settings()
        settings.set_property('enable-universal-access-from-file-uris', True)
        settings.set_property('enable-file-access-from-file-uris', True)
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

        window.show_all()
        self.window = window
        self.webkit_web_view = webkit_web_view
        self.webkit_main_frame = webkit_main_frame
        self.app_path = app_path

    def _url_map_to_function(self, url):
        match_list = list()
        for pattern in self.url_pattern:
            m = re.match(pattern, url)
            if m:
                match_list.append(m)

        if len(match_list) > 1:
            raise Exception('Found more than one matched urls')
            return None

        try:
            m = match_list[0]
        except:
            return None

        args = list(m.groups())
        kw = m.groupdict()
        for value in kw.values():
            args.remove(value)

        return self.url_pattern[m.re.pattern](*args, **kw)

    def route(self, pattern=None):
        def decorator(fn):
            self.url_pattern[pattern] = fn
            return fn
        return decorator

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
            print 'navigation_policy_decision_requested'

    def on_web_view_resource_request_starting(
            self,
            web_view,
            web_frame,
            web_resource,
            network_request,
            network_response=None):
        if self.debug is True:
            print 'web_view_resource_request_starting'

    def on_web_view_resource_response_received(
            self,
            web_view,
            web_frame,
            web_resource,
            network_response,
            *arg, **kw):
        if self.debug is True:
            print 'web_view_resource_response_received'

    def on_web_view_resource_load_finished(
            self,
            web_view, web_frame, web_resource,
            *args, **kw):
        if self.debug is True:
            print 'web_view_resource_load_finished'

    def on_web_frame_resource_request_starting(
            self,
            web_frame,
            web_resource,
            network_request,
            network_response=None):
        if self.debug is True:
            print 'web_frame_resource_request_starting'
        url = urlparse.unquote(network_request.get_uri())
        url = urlparse.urlparse(url.decode('utf-8'))
        if url.netloc == '':
            # Try mapping request path to function. `return`.
            # If there's no mapped function then serve it as static file.
            result = self._url_map_to_function(url.path)
            if result:
                # Make sure result is <tuple>
                if isinstance(result, unicode) or \
                        isinstance(result, str):
                    result = (result,)
                (content, mimetype) = response(*result)
                file_ext = mimetypes.guess_extension(mimetype)
                tmp_file_path = tempfile.mkstemp(suffix=file_ext)[1]
                f = codecs.open(tmp_file_path, 'w', encoding='utf-8')
                f.write(content)
                f.close()
                network_request.set_uri('file://' + tmp_file_path + '?tmp=1')
            else:
                # A bit hack about request url
                # Remove self.app_path string from url
                # This case happen if resource is called by static files
                # in relative path format ('./<path>')
                # for ex. images called by CSS.
                url_path = re.sub(self.app_path, '', url.path)

                # Remove /tmp/ path from url
                # This case happen with the file which was opened directly
                # from controller.
                splitted_path = url_path.split('/')
                if splitted_path[1] == 'tmp':
                    splitted_path.pop(1)
                url_path = os.path.join(*splitted_path)
                file_path = os.path.join(self.app_path, url_path)
                file_path = os.path.normcase(file_path)
                file_path = os.path.normpath(file_path)
                if not(os.path.exists(file_path)):
                    raise Exception('Not found: ' + file_path)
                network_request.set_uri('file://' + file_path)

    def on_web_frame_resource_response_received(
            self,
            web_frame,
            web_resource,
            network_response,
            *arg, **kw):
        if self.debug is True:
            print 'web_frame_resource_response_received'
        url = urlparse.urlparse(network_response.get_uri())
        url = urlparse.urlparse(url.path)
        query = urlparse.parse_qs(url.query)
        if 'tmp' in query:
            os.remove(url.path)

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

    def run(self):
        index = self._url_map_to_function('/')
        if self.debug is True:
            print self.app_path
        self.webkit_web_view.load_string(
            index,
            mime_type='text/html',
            encoding='utf-8',
            base_uri='/',
        )
        Gtk.main()


def response(content=None, mimetype='text/html'):
    """Make response tuple

    Potential features to be added
      - Parameters validation
    """
    return (content, mimetype)
