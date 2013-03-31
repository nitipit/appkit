#!/usr/bin/env python
from appkit.api.v0_2_6 import App, render_template

app = App(__name__)


@app.route('/')
def index():
    return render_template('index.html')

app.run()
