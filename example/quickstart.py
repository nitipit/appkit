from appkit.app import App

app = App()


@app.route('/$')
def root():
    return '<a href="app:///greeting/hello/world/">Welcome</a>'


@app.route('/greeting/(.+)/(.+)/')
def greeting(text1, text2):
    return text1 + ' ' + text2

app.run()
