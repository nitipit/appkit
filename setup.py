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
    name="AppKit",
    version="0.1",
    package_dir={'appkit': 'appkit'},
    packages=['appkit'],
    package_data={'appkit': data},
    install_requires=['sphinx_bootstrap_theme', ],
)
