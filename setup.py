from distutils.core import setup
import os

data = list()
for d in os.walk('appkit/'):
    if len(d[2]) > 0:
        path_list = map(
            lambda x: str.join('/', os.path.join(d[0], x).split('/')[1:]),
            d[2]
        )
        data.extend(path_list)

setup(
    name='AppKit',
    version='0.2',
    description='Desktop application framework based on Webkit, \
        HTML5, CSS3, Javascript and Python',
    author='Nitipit Nontasuwan',
    author_email='nitipit@gmail.com',
    url='http://nitipit.github.com/appkit/',
    license='MIT',
    platforms=['Linux', ],
    keywords=['framework, html5, gnome, ui'],
    package_dir={'appkit': 'appkit'},
    packages=['appkit'],
    package_data={'appkit': data},
    requires=['sphinx_bootstrap_theme', ],
)
