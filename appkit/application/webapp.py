#!/usr/bin/env python
from appkit.api.v0_2_6 import App, render_template

app = App(__name__)
settings = app.webkit_web_view.get_settings()
settings.set_property('enable-accelerated-compositing', True)
settings.set_property('enable-webgl', True)
settings.set_property('enable-smooth-scrolling', True)


@app.route('/')
def index():
    return render_template('index.html')
