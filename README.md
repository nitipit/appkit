# AppKit
> Application framework based on Webkit, HTML5 and Python

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
```