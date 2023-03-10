from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def text() -> str:
    input_filepath = Path(__file__).parent.parent / 'examples' / 'input.txt'
    with open(input_filepath, encoding='utf-8') as f:
        text = f.read()
    return text
