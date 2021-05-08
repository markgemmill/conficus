from pathlib import Path
import pytest

CWD = Path().resolve()
DOCS = Path(CWD, "test", "samples")


@pytest.fixture
def inhert_cfg():
    return Path(DOCS, "inheritance_sample.ini")


@pytest.fixture
def cfg_file():
    return Path(DOCS, "inheritance_sample.ini")
