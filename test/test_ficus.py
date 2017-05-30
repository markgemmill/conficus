import pytest
import ficus


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
    assert raw_cfg['with_opt']['hero'].value  == 'crosby'
    assert raw_cfg['with_opt']['game'].value == '7'

   
def test_raw_multiline_option_values(raw_cfg):
    assert isinstance(raw_cfg['with_opt.multiline'], ficus.ConfigValue)
    assert raw_cfg['with_opt.multiline'].is_multiline


def test_inheritence(raw_cfg):
    ficus.push_inheritence(raw_cfg)

    assert raw_cfg['inherited.one'].value == '1'
    assert raw_cfg['inherited.two'].value  == '2' 
    assert raw_cfg['inherited.three'].value == '3' 

    assert raw_cfg['inherited.parent.one'].value == '1'
    assert raw_cfg['inherited.parent.two'].value == '1' 
    assert raw_cfg['inherited.parent.three'].value == '2' 

    assert raw_cfg['inherited.parent.child.one'].value == '1'
    assert raw_cfg['inherited.parent.child.two'].value == '1'
    assert raw_cfg['inherited.parent.child.three'].value == '1'
