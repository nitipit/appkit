# AppKit
> Application framework based on Webkit, HTML5 and Python

## Installation:
Use Python `pip` command
```
$ pip install git+https://nitipit@bitbucket.org/nitipit/appkit.git
```

## Usage:
```
from appkit import App

app = App()

@app.route('/')
def home(app):
    app.webkit_web_view.load_string(
        '<a href="app:///webpage/">Webpage</a>',
        'text/html',
        'utf-8',
        ''
    )

@app.route('/webpage/')
def webpage(app):
    app.webkit_web_view.load_string(
    	'We are on Webpage !',
    	'text/html',
    	'utf-8',
    	''
    )
    
app.run()
```