#!/usr/bin/env python
from appkit.api.v0_2_4 import App

app = App(__file__)


@app.route('^/$')
def home():
    return '''
        <html>
        <head>
        <title>Routing</title>
        </head>
        <body>
        <a href="/sum/1/2/">sum</a>
        <br /> <a href="/greeting/Hello/Gnome/">greeting</a>
        </body>
        </html>
        '''


@app.route('/sum/(.+)/(.+)/')
def sum(arg1, arg2):
    return unicode(int(arg1) + int(arg2))


@app.route('/greeting/(?P<greeting>.+)/(?P<name>.+)/')
def greeting(*args, **kw):
    return kw['greeting'] + ' ' + kw['name']

app.run()
