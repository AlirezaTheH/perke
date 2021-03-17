import pytest
from os.path import (join,
                     dirname)


@pytest.fixture(scope='session')
def text():
    input_filepath = join(dirname(dirname(__file__)),
                          'examples',
                          'input.txt')
    with open(input_filepath) as f:
        text = f.read()
    return text
