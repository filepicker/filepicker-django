try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='django-filepicker',
    version='0.2.3',
    description='Official Filepicker Django Library',
    author='Filepicker.io',
    author_email='contact@filepicker.io',
    url='http://developers.filepicker.io/',
    packages=['django_filepicker'],
    install_requires=['django >= 1.3','requests'],
    license="BSD",
    zip_safe=False,
)
