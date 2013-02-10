#!/usr/bin/env python

from appkit.app import App

app = App(__file__)


@app.route('^/$')
def home():
    return '<a href="/test/Hello/World/" />Link</a>'


@app.route('/test/(.+)/(.+)/')
def test(text1=None, text2=None):
    return ('<h1>' + text1 + ' ' + text2 + '</h1>', 'text/html')

app.run()
