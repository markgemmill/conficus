from conficus.structs import ConfigDict
from conficus.walk import walk_config

src_dict = {
    "app": {"level_1": 1, "level_2a": {"level_2": 2, "level_3a": {"level_3": 3}}}
}


def test_configdict_init():
    c = ConfigDict(src_dict)

    assert isinstance(c, ConfigDict)
    assert isinstance(c["app"], ConfigDict)
    assert isinstance(c["app.level_2a"], ConfigDict)
    assert isinstance(c["app.level_2a.level_3a"], ConfigDict)

    level_3 = c["app.level_2a.level_3a"]
    level_3["level_4a"] = {"level_4": 4}

    assert isinstance(c["app.level_2a.level_3a.level_4a"], ConfigDict)


def test_configdict_contains():
    c = ConfigDict(src_dict)
    assert "app" in c
    assert "app.level_2a" in c
    assert "app.level_2a.error" not in c
    assert 23 not in c


def test_configdict_walk():
    c = ConfigDict(src_dict)

    expected = [1, 2, 3]
    expected_key = ["level_1", "level_2", "level_3"]
    level = 0
    for _, _, key, value in walk_config(c):
        print(key)
        assert key == expected_key[level]
        assert value == expected[level]
        level += 1


def test_configdict_walk_with_full_keys():
    c = ConfigDict(src_dict)

    expected = [1, 2, 3]
    expected_key = [
        "app.level_1",
        "app.level_2a.level_2",
        "app.level_2a.level_3a.level_3",
    ]
    level = 0
    for _, full_key, key, value in walk_config(c):
        print(full_key)
        assert full_key == expected_key[level]
        assert value == expected[level]
        level += 1
