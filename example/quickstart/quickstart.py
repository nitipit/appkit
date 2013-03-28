#!/usr/bin/env python
from appkit.api.v0_2_4 import App

app = App(__name__)


@app.server.route('/')
def index():
    return '<a href="/test/">hello</a>'


@app.server.route('/test/')
def test():
    return 'test'

app.run()
