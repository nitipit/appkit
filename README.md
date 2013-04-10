AppKit
======

> Gnome desktop application framework based on Webkit, HTML5, CSS3,
> Javascript and Python

"AppKit" will be a framework for gnome desktop application powered by
[WebKit](http://www.webkit.org/) engine, which means we can bring web
technology such as HTML5, CSS3, Javascript and Web browser engine to
desktop.

Full Documentation
------------------

[https://appkit.readthedocs.org/en/latest](https://appkit.readthedocs.org/en/latest)/

Target Platforms
----------------

Linux

Installation
------------

### Option 1: From PyPI (Release version)

    $ pip install appkit

### Option 2: From Git

    $ pip install git+git://github.com/nitipit/appkit.git

Quick Start
-----------

    #!/usr/bin/env python

    from appkit.api.v0_2_6 import App

    app = App(__name__)


    @app.route(/)
    def home():
        return '<a href="/test/Hello/World/" />Link</a>'


    @app.route('/test/text1/text2/')
    def test(text1=None, text2=None):
        return ('<h1>' + text1 + ' ' + text2 + '</h1>', 'text/html')

    app.run()
