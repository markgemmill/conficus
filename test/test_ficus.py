import pytest
import ficus


def test_section_parsing(config_file):

    lines = ficus.read_config(str(config_file))
    origin, conf = ficus.parse_raw(lines)

    assert isinstance(origin, list)
    assert isinstance(conf, dict)

    # test basic section
    assert origin[0][0] == 'section'
    assert origin[0][1] == '[root_section]'
    assert origin[0][2] == 'root_section'
    assert origin[0][3] == {}

    # test hierarchic section
    assert origin[1][0] == 'section'
    assert origin[1][1] == '[root.leaf]'
    assert origin[1][2] == 'root.leaf'
    assert origin[1][3] == {'sub': {}}

    # test hierarchic section
    assert origin[2][0] == 'section'
    assert origin[2][1] == '[root.leaf.sub]'
    assert origin[2][2] == 'root.leaf.sub'
    assert origin[2][3] == {}

    assert conf['root_section'] == {} 

    # test call types
    assert conf['root']['leaf']['sub'] == {} 
    assert conf['root.leaf.sub'] == {} 

    assert conf['root']['leaf'] == {'sub': {}} 
    assert conf['root.leaf'] == {'sub': {}} 

    # blank line
    assert origin[3][0] == None

    assert origin[4][0] == 'comment'

    assert conf['with_opt']['name'] == 'penguins for stanley'
    assert conf['with_opt']['hero'] == 'crosby'
    assert conf['with_opt']['game'] == '7'

    assert conf['with_opt.name'] == 'foo'
    
