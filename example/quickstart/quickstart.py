#!/usr/bin/env python
from appkit.api.v0_2_4 import App
import codecs

app = App(__file__)


@app.route('^/$')
def index():
    html = codecs.open('ui.html', 'r', encoding='utf8').read()
    return html


@app.route('/test/(.+)/(.+)/')
def test(text1=None, text2=None):
    return ('<h1>' + text1 + ' ' + text2 + '</h1>', 'text/html')

app.run()
