from decimal import Decimal
from pathlib import Path
import pytest
import conficus
from conficus.coerce import handle_custom_coercers


def test_handle_custom_coercers_with_regex_error(capsys):
    with pytest.raises(Exception) as ex:
        [c for c in handle_custom_coercers([("int", (r"^\d+$", str))])]

    assert "must contain a named group" in str(ex.value)


def test_handle_custom_coercers_with_converter_error():
    with pytest.raises(Exception) as ex:
        [c for c in handle_custom_coercers([("int", (r"^(?P<value>\d+)$", "4"))])]
    assert "must be callable" in str(ex.value)


def test_coerce_path():
    CFG = r"""
[path]
windows1 = 'C:\some\drive'
windows2 = 'C:'
windows3 = "C:\\"
unix1 = '/some/drive'
unix2 = '/'
non_str = 1000
    """
    config = conficus.load(CFG, pathlib=True)

    assert isinstance(config["path.windows1"], Path)
    assert isinstance(config["path.windows2"], Path) is False
    assert isinstance(config["path.windows3"], Path)
    assert isinstance(config["path.unix1"], Path)
    assert isinstance(config["path.unix2"], Path)


def test_coerce_custom_coercer():
    config = conficus.load("integer = '5'")
    assert config["integer"] == "5"

    config = conficus.load(
        "integer = '5'", coercers=[("int", (r"^(?P<value>\d+)$", str))]
    )
    assert config["integer"] == "5"


def test_coerce_decimal_str():
    config = conficus.load("integer = '5.5'", decimal=True)
    assert config["integer"] == Decimal("5.5")


def test_coerce_custom_additional():
    config = conficus.load("integer = '5.5'", decimal=True, pathlib=True)
    assert config["integer"] == Decimal("5.5")

    config = conficus.load(
        "integer = '5.5'",
        coercers=[("decimal", (r"^(?P<value>\d+\.\d+)$", str))],
        decimal=True,
        pathlib=True,
    )
    assert config["integer"] == "5.5"
