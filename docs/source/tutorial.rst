Tutorial
========

What AppKit do, really
----------------------
The main task for ``AppKit`` is to make HTML5 on Webkit interact smoothly with Python which is better at dealing with desktop environment

The smallest application with HTML5
-----------------------------------


Directory structure
~~~~~~~~~~~~~~~~~~~
::

    quickstart/
    |-- quickstart.py
    `-- ui.html


User interface with HTML5
~~~~~~~~~~~~~~~~~~~~~~~~~
ui.html


.. code-block:: html

    <html>
    <head><title>AppKit</title></head>
    <body>
    Hello AppKit
    </body>
    </html>


Initialize application by Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
quickstart.py


.. code-block:: python

    from appkit.api.v0_2_4 import App
    import codecs
    
    app = App(__file__)

    @app.route('^/$')
    def index():
        html = codecs.open('ui.html', 'r', encoding='utf8').read()
        return html

    app.run()

Now you can run
~~~~~~~~~~~~~~~

::

    $ python app.py

.. image:: _static/tutorial/quick-app.png
