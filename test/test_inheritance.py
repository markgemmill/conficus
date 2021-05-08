import pytest
import conficus


def test_basic_inheritance(inhert_cfg):
    config = """
[app]
level_1 = 1

[app.level_2a]
level_2 = 2

[app.level_2a.level_3a]
level_3 = 3

[app.level_2a.level_3a.level_4a]
level_4 = 4
"""
    cfg = conficus.load(config, inheritance=True)

    # sanity checks
    assert cfg["app.level_1"] == 1
    assert cfg["app.level_2a.level_2"] == 2
    assert cfg["app.level_2a.level_3a.level_3"] == 3
    assert cfg["app.level_2a.level_3a.level_4a.level_4"] == 4

    # level 2 inherits level 1 ?
    assert "level_1" in cfg["app.level_2a"]

    # level 3 inherits level 1 and 2
    assert "level_1" in cfg["app.level_2a.level_3a"]
    assert "level_2" in cfg["app.level_2a.level_3a"]

    # level 4 inherits level 1, 2 and 3
    assert "level_1" in cfg["app.level_2a.level_3a.level_4a"]
    assert "level_2" in cfg["app.level_2a.level_3a.level_4a"]
    assert "level_3" in cfg["app.level_2a.level_3a.level_4a"]


def test_inheritance_directive_no_inherit(inhert_cfg):
    config = """
[app]
level_1 = 1

[app.level_2a]
_inherit = 0
level_2 = 2

[app.level_2a.level_3a]
_inherit = 0
level_3 = 3

[app.level_2a.level_3a.level_4a]
_inherit = 0
level_4 = 4
"""
    cfg = conficus.load(config, inheritance=True)

    # sanity checks
    assert cfg["app.level_1"] == 1
    assert cfg["app.level_2a.level_2"] == 2
    assert cfg["app.level_2a.level_3a.level_3"] == 3
    assert cfg["app.level_2a.level_3a.level_4a.level_4"] == 4

    # level 2 inherits level 1 ?
    assert "level_1" not in cfg["app.level_2a"]

    # level 3 inherits level 1 and 2
    assert "level_1" not in cfg["app.level_2a.level_3a"]
    assert "level_2" not in cfg["app.level_2a.level_3a"]

    # level 4 inherits level 1, 2 and 3
    assert "level_1" not in cfg["app.level_2a.level_3a.level_4a"]
    assert "level_2" not in cfg["app.level_2a.level_3a.level_4a"]
    assert "level_3" not in cfg["app.level_2a.level_3a.level_4a"]


def test_inheritance_directive_inherit_one_level(inhert_cfg):
    config = """
[app]
level_1 = 1

[app.level_2a]
_inherit = 1 
level_2 = 2

[app.level_2a.level_3a]
_inherit = 1 
level_3 = 3

[app.level_2a.level_3a.level_4a]
_inherit = 1 
level_4 = 4
"""
    cfg = conficus.load(config, inheritance=True)

    # sanity checks
    assert cfg["app.level_1"] == 1
    assert cfg["app.level_2a.level_2"] == 2
    assert cfg["app.level_2a.level_3a.level_3"] == 3
    assert cfg["app.level_2a.level_3a.level_4a.level_4"] == 4

    # level 2 inherits level 1 ?
    assert "level_1" in cfg["app.level_2a"]

    # level 3 inherits level 1 and 2
    assert "level_1" not in cfg["app.level_2a.level_3a"]
    assert "level_2" in cfg["app.level_2a.level_3a"]

    # level 4 inherits level 1, 2 and 3
    assert "level_1" not in cfg["app.level_2a.level_3a.level_4a"]
    assert "level_2" not in cfg["app.level_2a.level_3a.level_4a"]
    assert "level_3" in cfg["app.level_2a.level_3a.level_4a"]


def test_inheritance_invalid_inherit_flag():
    config = """
[app]
level_1 = 1

[app.level_2a]
_inherit = 23.2 
level_2 = 2

[app.level_2a.level_3a]
_inherit = 1 
level_3 = 3

[app.level_2a.level_3a.level_4a]
_inherit = 1 
level_4 = 4
"""
    with pytest.raises(Exception):
        conficus.load(config, inheritance=True)
