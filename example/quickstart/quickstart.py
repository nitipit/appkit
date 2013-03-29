#!/usr/bin/env python
from appkit.api.v0_2_6 import App

app = App(__name__)


@app.route('/')
def index():
    return '<a href="/test/">hello</a>'


@app.route('/test/')
def test():
    return 'test'

app.run()
