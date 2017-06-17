from datetime import datetime
import ficus
from ficus.parse import FicusDict


def test_ficus_count_config_values(coerce_cfg):
    items = [i for i in coerce_cfg.walk_values()]
    assert len(items) == 21


def test_ficus_coerce_numbers(coerce_cfg):
    config = ficus.coerce(coerce_cfg)

    assert type(config) == FicusDict
    assert config['integer.value'] == 1
    assert config['float.value'] == 2.0


def test_ficus_coerce_lists(coerce_cfg):
    config = ficus.coerce(coerce_cfg)

    assert config['empty-list.value'] == []
    assert config['single-line-list.integers'] == [1, 2, 3, 4]
    assert config['single-line-list.floats'] == [3.4, 3.4]
    assert config['single-line-list.strings'] == ['one', 'two', 'three']


def test_ficus_coerce_boolean(coerce_cfg):
    config = ficus.coerce(coerce_cfg)

    assert config['bool-true.val1'] is True
    assert config['bool-true.val2'] is True
    assert config['bool-true.val3'] is True
    assert config['bool-true.val4'] is True
    assert config['bool-true.val5'] is True
    assert config['bool-true.val6'] is True


def test_ficus_coerce_datetime(coerce_cfg):
    config = ficus.coerce(coerce_cfg)

    assert isinstance(config['datetime.value'], datetime)
    assert config['datetime.value'].year == 2017
    assert config['datetime.value'].hour == 10


def test_ficus_coerce_date(coerce_cfg):
    config = ficus.coerce(coerce_cfg)

    assert isinstance(config['date.value'], datetime)
    assert config['date.value'].year == 2017
    assert config['date.value'].hour == 0


def test_ficus_coerce_time(coerce_cfg):
    config = ficus.coerce(coerce_cfg)

    assert isinstance(config['time.value'], datetime)
    assert config['time.value'].year == 1900
    assert config['time.value'].hour == 10
    assert config['time.value'].minute == 15
    assert config['time.value'].second == 2


def test_ficus_coerce_multiline(multiline_cfg):
    config = ficus.coerce(multiline_cfg)

    assert len(config['multiline.list-of-strings']) == 4
    assert config['multiline.list-of-strings'][0] == 'Wonder Woman'

    assert len(config['multiline.list-of-int']) == 4
    assert isinstance(config['multiline.list-of-int'][0], int)

    assert len(config['multiline.list-of-float']) == 4
    assert isinstance(config['multiline.list-of-float'][0], float)

    assert len(config['multiline.list-of-lists']) == 2
    assert isinstance(config['multiline.list-of-lists'][0], list)

    assert len(config['multiline.text']) == 163
    assert isinstance(config['multiline.text'], str)
