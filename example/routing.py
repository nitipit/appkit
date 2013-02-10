#!/usr/bin/env python
from appkit import App

app = App(__file__)


@app.route('^/$')
def home():
    return '<a href="/sum/1/2/">sum</a>' + \
        '<br /> <a href="/greeting/Hello/Gnome/">greeting</a>'


@app.route('/sum/(.+)/(.+)/')
def sum(arg1, arg2):
    return unicode(int(arg1) + int(arg2))


@app.route('/greeting/(?P<greeting>.+)/(?P<name>.+)/')
def greeting(*args, **kw):
    return kw['greeting'] + ' ' + kw['name']

app.run()
