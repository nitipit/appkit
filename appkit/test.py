#!/usr/bin/env python

from appkit.app import App, response

app = App()


@app.route('/')
def home():
    return '<a href="app:///test/" />Link</a>'


@app.route('/test/')
def test():
    return ('<h1>Hello World</h1>', 'application/json', 'utf-8')

app.run()
