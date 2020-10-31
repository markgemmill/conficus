import pytest
import conficus

CONFIG = {
        "": '''
[app]
debug = True

[email]
server = smtp.email.com
user = smtp-admin
password = smtp-password

[email.errors]
to = [admin@email.com]
cc = []

''',

    "toml": '''
[app]
debug = true

[email]
server = "smtp.email.com"
user = "smtp-admin"
password = "smtp-password"

[email.errors]
to = ["admin@email.com"]
cc = []

'''
}


@pytest.mark.parametrize("toml,cfg", [(False, ""), (True, "toml")])
def test_load_defaults(toml, cfg):
    print(toml, cfg)
    config = conficus.load(CONFIG[cfg], toml=toml)

    # sanity check
    assert config['app.debug'] is True

    # validate no inheritence
    assert 'server' not in config['email.errors']

    # validate config is readonly
    assert config.readonly is True


def test_read_config(cfg_pth):
    from os import environ
    PATH = str(cfg_pth['config'])
    environ['FICUS_LOAD_PATH_TEST'] = PATH
    with open(PATH, 'r') as fh_:
        CONTENT = fh_.read()

    config_from_path = conficus.read_config(PATH)
    config_from_env_var = conficus.read_config('FICUS_LOAD_PATH_TEST')
    config_from_string = conficus.read_config(CONTENT)

    assert config_from_path == config_from_string
    assert config_from_env_var == config_from_string


@pytest.mark.parametrize("toml,cfg", [(False,""), (True, "toml")])
def test_load_with_inheritence(toml, cfg):

    config = conficus.load(CONFIG[cfg], inheritance=True, toml=toml)

    # sanity check
    assert config['app.debug'] is True

    # validate inheritence took place
    assert 'server' in config['email.errors']

    # validate config is readonly
    assert config.readonly is True


@pytest.mark.parametrize("toml,cfg", [(False,""), (True, "toml")])
def test_load_with_non_readonly(toml, cfg):

    print(toml, cfg)
    print(CONFIG[cfg])

    config = conficus.load(CONFIG[cfg], inheritance=True, readonly=False, toml=toml)

    # sanity check
    assert config['app.debug'] is True

    # validate no inheritence
    assert 'server' in config['email.errors']

    # validate config is readonly
    assert hasattr(config, 'readonly') is False
