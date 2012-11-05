#!/usr/bin/env python

from appkit import App
import os

app = App()


@app.route('/')
def home():
    return ('<a href="app:///test/" />Link</a>', 'text/html')


@app.route('/test/')
def test():
    return ('<h1>Hello World !</h1>', 'text/html')

app.run()
