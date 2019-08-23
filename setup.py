from setuptools import setup


setup(
    name='kratos-dpi',
    packages=[
        "kratos_dpi"
    ],
    version='0.0.1',
    author='Keyi Zhang',
    author_email='keyi@stanford.edu',
    description='kratos-dpi is a plugin for kratos that supports running arbitrary Python code via DPI',
    url="https://github.com/Kuree/kratos-dpi",
    install_requires=[
        "kratos",
    ],
)
