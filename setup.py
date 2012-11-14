from distutils.core import setup

setup(
    name='django-xhrforms',
    version='0.1.0',
    author='Aron Jones',
    author_email='aron.jones@gmail.com',
    packages=['xhrforms'],
    url='https://github.com/Shopcaster/django-xhr-form',
    license='LICENSE.txt',
    description='Simple XHR form validation in Django.',
    long_description=open('README.md').read(),
    install_requires=[
        "Django >= 1.4.0",
    ],
)
