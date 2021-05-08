import conficus


def test_conficus_load_filepath(cfg_file):
    cfg = conficus.load(cfg_file)
    assert cfg["app.level_1"] == 1


def test_conficus_load_filepath_string(cfg_file):
    cfg = conficus.load(str(cfg_file))
    assert cfg["app.level_1"] == 1


def test_conficus_load_from_environ(cfg_file):
    from os import environ

    environ["FICUS_LOAD_PATH_TEST"] = str(cfg_file)

    cfg = conficus.load("FICUS_LOAD_PATH_TEST")
    assert cfg["app.level_1"] == 1
