import conficus

CONFIG = '''
[app]
debug = True

[email]
server = smtp.email.com
user = smtp-admin
password = smtp-password

[email.errors]
to = [admin@email.com]
cc = []

'''


def test_ficus_load_defaults():

    config = conficus.load(CONFIG)

    # sanity check
    assert config['app.debug'] is True

    # validate no inheritence
    assert 'server' not in config['email.errors']

    # validate config is readonly
    assert config.readonly is True


def test_ficus_load_with_inheritence():

    config = conficus.load(CONFIG, inheritance=True)

    # sanity check
    assert config['app.debug'] is True

    # validate inheritence took place
    assert 'server' in config['email.errors']

    # validate config is readonly
    assert config.readonly is True


def test_ficus_load_with_non_readonly():

    config = conficus.load(CONFIG, inheritance=True, readonly=False)

    # sanity check
    assert config['app.debug'] is True

    # validate no inheritence
    assert 'server' in config['email.errors']

    # validate config is readonly
    assert hasattr(config, 'readonly') is False
