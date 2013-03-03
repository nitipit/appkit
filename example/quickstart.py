#!/usr/bin/env python
from appkit import App

app = App(__file__)


@app.route('^/$')
def home():
    return '''
        <html>
        <head>
        <title>Quick Start</title>
        </head>
        <body>
        <a href="/test/Hello/World/">Link</a>
        </body>
        </html>
        '''


@app.route('/test/(.+)/(.+)/')
def test(text1=None, text2=None):
    return ('<h1>' + text1 + ' ' + text2 + '</h1>', 'text/html')

app.run()
