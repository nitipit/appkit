#!/usr/bin/env python

from appkit.app import App, response

app = App()


@app.route('/')
def home():
    return response('<a href="app:///test/" />Link</a>')


@app.route('/test/')
def test():
    return response('<h1>Hello World</h1>')

app.run()
