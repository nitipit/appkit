# AppKit
> Application framework based on Webkit, HTML5 and Python

## Installation:
Use Python `pip` command
```
$ pip install git+https://nitipit@bitbucket.org/nitipit/appkit.git
```

## Usage:
```
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
```

![screenshot-1](https://raw.github.com/nitipit/appkit/master/doc/1.png)
![screenshot-2](https://raw.github.com/nitipit/appkit/master/doc/2.png)