"""Package this project."""
import json
import re
from configparser import ConfigParser

from setuptools import find_packages, setup

import medium_crawler

config = ConfigParser()
config.read('Pipfile')
with open('Pipfile.lock') as f:
    pipfile_lock = json.load(f)
install_requires = []
for k, v in pipfile_lock['default'].items():
    if 'git' in v:
        ver = re.search('ref = "(.+?)"', config['packages'][k]).group(1)
        pkg = '{}==git+{}@{}'.format(k.replace('-', '_'), v['git'], ver)
    else:
        pkg = k + v['version']
    install_requires.append(pkg)

setup(
    name='medium-crawler',
    version=medium_crawler.__version__,
    packages=find_packages(),
    entry_points={'scrapy': ['settings = medium_crawler.settings']},
    install_requires=install_requires,
)
