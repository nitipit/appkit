#!/usr/bin/env python
# coding=utf8

from appkit.app import App

app = App()


@app.route('/')
def home():
    return u'<a href="app:///test/สวัสดี/" />Link</a>'


@app.route('/test/(.*)/')
def test(text=None):
    print type(text)
    return ('<h1>' + text + '</h1>', 'text/html')

app.run()
