import os
import pytest
from pathlib import Path
import ficus


CWD = Path().resolve()


@pytest.fixture
def raw_cfg():
    pth = Path(CWD, r'test', 'config.txt')
    lines = ficus.read_config(str(pth))
    return ficus.parse_raw(lines)
