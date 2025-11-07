import conficus
from conficus.walk import walk_config


def test_walk_config():
    CFG = r"""
level_1_a = 'one'

[level_2]
level_2_a = 'two-eh'

[level_2.level_3]
level_3_a = 'three-eh'

[[level_4]]
level_4_a = 'four-eh'

[[level_4]]
level_4_b = 'four-bee'

[[level_4]]
level_4_c = 'four-cee'
"""
    config = conficus.load(CFG, pathlib=True)

    print(config)
    expected_output = [
        "level_1_a='one'",
        "level_2.level_2_a='two-eh'",
        "level_2.level_3.level_3_a='three-eh'",
        "level_4.0.level_4_a='four-eh'",
        "level_4.1.level_4_b='four-bee'",
        "level_4.2.level_4_c='four-cee'",
    ]

    index = 0
    for parent, path, key, value in walk_config(config):
        assert f"{path}='{value}'" == expected_output[index]
        index += 1
