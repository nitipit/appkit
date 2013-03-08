AppKit
======

> Gnome desktop application framework based on Webkit, HTML5, CSS3,
> Javascript and Python

"AppKit" will be a framework for gnome desktop application powered by
[WebKit](http://www.webkit.org/) engine, which means we can bring web
technology such as HTML5, CSS3, Javascript and Web browser engine to
desktop.

Target Platforms
----------------

Linux

Installation
------------

### PyPI (Release version)

    $ pip install appkit

### Git

    $ pip install git+git://github.com/nitipit/appkit.git

Quick Start
-----------

example:

    #!/usr/bin/env python

    from appkit.api.v0_2_4 import App

    app = App(__file__)


    @app.route('^/$')
    def home():
        return '<a href="/test/Hello/World/" />Link</a>'


    @app.route('/test/(.+)/(.+)/')
    def test(text1=None, text2=None):
        return ('<h1>' + text1 + ' ' + text2 + '</h1>', 'text/html')

    app.run()

![image](https://raw.github.com/nitipit/appkit/master/docs/1.png)
![image](https://raw.github.com/nitipit/appkit/master/docs/2.png)
