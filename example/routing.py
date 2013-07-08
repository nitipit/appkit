#!/usr/bin/env python
from appkit.api.v0_2_6 import App

app = App(__name__)


@app.route('/')
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


@app.route('/sum/<arg1>/<arg2>/')
def sum(arg1, arg2):
    return str(int(arg1) + int(arg2))


@app.route('/greeting/<greeting>/<name>/')
def greeting(greeting, name):
    return greeting + ' ' + name

app.run()
