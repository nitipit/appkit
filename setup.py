from distutils.core import setup
import os
import appkit

data = list()
for d in os.walk('appkit/'):
    if len(d[2]) > 0:
        path_list = map(
            lambda x: str.join('/', os.path.join(d[0], x).split('/')[1:]),
            d[2]
        )
        data.extend(path_list)

#if subprocess.call(['python', '-m', 'unittest', 'discover', '-v']):
#    print('================================================================')
#    print('AppKit doesn\'t pass test in your environment')
#    print('Some functionallity might not work correctly')
#    print('================================================================')

setup(
    name='AppKit',
    version=appkit.__version__,
    description='Desktop application framework based on Webkit' +
    ' HTML5, CSS3, Javascript and Python',
    author='Nitipit Nontasuwan',
    author_email='nitipit@gmail.com',
    url='http://nitipit.github.com/appkit/',
    license='MIT',
    platforms=['Linux', ],
    keywords=['framework, html5, gnome, ui'],
    package_dir={'appkit': 'appkit'},
    packages=['appkit'],
    package_data={'appkit': data},
    install_requires=['sphinx_bootstrap_theme', 'beautifulsoup4'],
)
