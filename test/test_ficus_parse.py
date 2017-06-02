import pytest
import ficus


def test_ficus_dict_contains():

    d = ficus.FicusDict()
    d['one'] = ficus.FicusDict()
    d['one']['two'] = ficus.FicusDict()
    d['one']['two']['name'] = 'name'

    assert 'one' in d
    assert 'two' not in d
    assert 'one.two' in d
    assert 'one.three' not in d
    assert 'one.two.name' in d
    assert 'one.two.who' not in d


def test_ficus_invalid_indent():
    raw_lines = [
        '[section]\n',
        '# comment line\n',
        '      a line on its own.\n',
        ]

    with pytest.raises(Exception):
        ficus.parse_raw(raw_lines)


def test_ficus_dict_iter(raw_cfg):
    items = [i for i in raw_cfg.iter()]
    assert len(items) == 10
    assert items[0].value == 'penguins for stanley'
    assert items[9].value == '1'


def test_section_parsing(raw_cfg):

    assert isinstance(raw_cfg, dict)

    assert 'root_section' in raw_cfg
    assert 'root.leaf' in raw_cfg
    assert 'root.leaf.sub' in raw_cfg
    assert 'with_opt' in raw_cfg


def test_section_defaults(raw_cfg):
    assert raw_cfg['root_section'] == {}

    assert raw_cfg['root']['leaf'] == {'sub': {}}
    assert raw_cfg['root']['leaf']['sub'] == {}

    assert raw_cfg['root.leaf'] == {'sub': {}}
    assert raw_cfg['root.leaf.sub'] == {}


def test_raw_option_values(raw_cfg):
    assert raw_cfg['with_opt']['name'].value == 'penguins for stanley'
    assert raw_cfg['with_opt']['hero'].value == 'crosby'
    assert raw_cfg['with_opt']['game'].value == '7'


def test_raw_multiline_option_values(raw_cfg):
    assert isinstance(raw_cfg['with_opt.multiline'], ficus.ConfigValue)
    assert raw_cfg['with_opt.multiline'].multiline
