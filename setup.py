# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in erpnext_telegram/__init__.py
from erpnext_telegram import __version__ as version

setup(
	name='erpnext_telegram',
	version=version,
	description='ERPNext Telegram Integration',
	author='Adam Dawoodjee',
	author_email='adam@erp.co.zm',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
