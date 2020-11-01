from decimal import Decimal
from pathlib import Path
import conficus
import conficus.toml
from conficus.coerce import UNIX_PATH_REGEX
from conficus.coerce import WINDOWS_PATH_REGEX
from conficus.parse import matcher


def assert_toml_values(cfg):
    assert cfg["boolean"] is True
    assert cfg["float"] == 10.12
    assert cfg["date"].month == 10
    assert cfg["date-and-time"].minute == 12
    assert cfg["list"][0] == "Herb"
    assert cfg["string"].startswith("A wealthy")
    assert cfg["email"]["server"] == "smtp.server.com"
    assert cfg["email"]["notify"]["to"] == "notify@home.biz"
    assert cfg["email.server"] == "smtp.server.com"
    assert cfg["email.notify.to"] == "notify@home.biz"


def test_toml_parse(toml_pth):
    cfg = conficus.toml.parse(conficus.read_config(toml_pth))
    assert_toml_values(cfg)
    assert cfg["decimal"] == "10.12"


def test_toml_coerce_decimal(toml_pth):
    cfg = conficus.toml.parse(conficus.read_config(toml_pth))
    cfg = conficus.toml.coerce(cfg, decimal=True)
    assert_toml_values(cfg)
    assert cfg["decimal"] == Decimal("10.12")


def test_toml_coerce_path(toml_pth):
    cfg = conficus.toml.parse(conficus.read_config(toml_pth))
    cfg = conficus.toml.coerce(cfg, decimal=True, pathlib=True)
    assert_toml_values(cfg)
    assert isinstance(cfg["unix-file-path"], Path)
    assert isinstance(cfg["windows-file-path"], Path)


custom_coercers = [
    ("win_path", (WINDOWS_PATH_REGEX, lambda x: "windows path converted")),
    ("other_path", (UNIX_PATH_REGEX, lambda x: "unix path converted")),
]


def test_toml_custom_coercers(toml_pth):
    cfg = conficus.load(
        toml_pth, decimal=True, pathlib=True, toml=True, coercers=custom_coercers
    )
    assert_toml_values(cfg)
    assert cfg["windows-file-path"] == "windows path converted"
    assert cfg["unix-file-path"] == "unix path converted"
