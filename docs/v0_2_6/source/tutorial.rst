Tutorial
========

What AppKit do, really
----------------------
The main task for ``AppKit`` is to make HTML5 on Webkit interact smoothly with Python to deal with Gnome desktop environment

Quick application with templates
--------------------------------


Directory structure
~~~~~~~~~~~~~~~~~~~
::

    quickstart/
    ├── quickstart.py
    └── templates
        └── index.html


User interface with HTML5
~~~~~~~~~~~~~~~~~~~~~~~~~
index.html


.. code-block:: html

    <!DOCTYPE html>
    <head><title>AppKit</title></head>
    <body>
    Hello AppKit
    </body>
    </html>


Initialize application by Python
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
quickstart.py


.. code-block:: python

    #!/usr/bin/env python
    from appkit.api.v0_2_6 import App, render_template

    app = App(__name__)


    @app.route('/')
    def index():
        return render_template('index.html')

    app.run()

Now you can run
~~~~~~~~~~~~~~~

::

    $ python app.py

.. image:: _static/tutorial/quick-app.png
