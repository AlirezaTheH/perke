from os.path import dirname, join

import pytest


@pytest.fixture(scope='session')
def text() -> str:
    input_filepath = join(dirname(dirname(__file__)), 'examples', 'input.txt')
    with open(input_filepath) as f:
        text = f.read()
    return text
