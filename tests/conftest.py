"""Pytest's conftest.py."""
import logging
import os

import betamax
import pytest

from medium_crawler import color_formatter

CASSETTE_DIR = 'tests/cassettes/'

if not os.path.exists(CASSETTE_DIR):
    os.mkdir(CASSETTE_DIR)
    print(f'"{CASSETTE_DIR}" created!')

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = CASSETTE_DIR


@pytest.fixture(scope='session', autouse=True)
def setup_logging():
    """Set custom logging handler for pytest."""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    _handler = logging.StreamHandler()
    _handler.setFormatter(color_formatter)
    logger.addHandler(_handler)
