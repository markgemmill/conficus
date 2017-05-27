import os
import pytest
from pathlib import Path


CWD = Path().resolve()


@pytest.fixture
def config_file():
    return Path(CWD, r'test\config.txt')
