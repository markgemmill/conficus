from pathlib import Path
import pytest
import ficus


CWD = Path().resolve()
DOCS = Path(CWD, 'test', 'docs')
PATHS = {
    'config': Path(DOCS, 'config.txt'),
    'coerce': Path(DOCS, 'config_coerce.txt'),
    'multiline': Path(DOCS, 'config_multiline.txt')
}


@pytest.fixture
def cfg_pth():
    return PATHS


@pytest.fixture
def raw_cfg():
    lines = ficus.read_config(str(PATHS['config']))
    return ficus.parse(lines)


@pytest.fixture
def coerce_cfg():
    lines = ficus.read_config(str(PATHS['coerce']))
    return ficus.parse(lines)


@pytest.fixture
def multiline_cfg():
    lines = ficus.read_config(str(PATHS['multiline']))
    return ficus.parse(lines)
