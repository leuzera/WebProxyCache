# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

setup(
    name='proxycache',
    version='0.1.0',
    description='Trabalho para a classe de Redes de Computadores 1, 2018/1 - INF/UFG',
    long_description=readme,
    author='Leonardo M Fleury',
    author_email='fleuryleomoraes@gmailcom',
    url='https://github.com/leuzera/proxycache',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

