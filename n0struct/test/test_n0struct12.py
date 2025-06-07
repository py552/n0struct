import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")

from n0struct import (
    n0print,
    n0debug,
    n0debug_calc,
    init_logger,
    # n0dict,
    # n0list,
    n1dict,
    n1list,
)
import json

def test_n1dict_n1list():
    assert1 = [
        {'name': 'John', 'tags': 'admin'},
        {'name': 'Jane', 'tags': ['user', 'active']}
    ]
    _list = n1list(assert1)
    # n0debug("_list")
    n0print(f"assert1 = {_list.to_json()}")
    assert json.dumps(_list, sort_keys=True) == json.dumps(assert1, sort_keys=True)
    
    n0print(_list.to_json())
    n0print(_list.to_xml())
    n0print(_list.to_xpath())

    result = _list['[0]']
    n0print(f"assert2 = {n1dict(result).to_json()}")
    assert2 = { "name": "John", "tags": "admin" }
    assert json.dumps(result, sort_keys=True) == json.dumps(assert2, sort_keys=True)

    result = _list['0']
    n0print(f"assert3 = {n1dict(result).to_json()}")
    assert json.dumps(result, sort_keys=True) == json.dumps(assert2, sort_keys=True)

    result = _list['[0]/name']
    n0print(f"assert4 = \"{result}\"")
    assert4 = "John"
    assert json.dumps(result, sort_keys=True) == json.dumps(assert4, sort_keys=True)

    result = _list['[0]/tags']
    n0print(f"assert5 = \"{result}\"")
    assert5 = "admin"
    assert json.dumps(result, sort_keys=True) == json.dumps(assert5, sort_keys=True)

    _list['[1]/tags[1]'] = 'passive1'
    result = _list['[1]/tags']
    n0print(f"assert6 = {result}")
    assert6 = ["user", "passive1"]
    assert json.dumps(result, sort_keys=True) == json.dumps(assert6, sort_keys=True)

    _list['1/tags[1]'] = 'passive2' # FIXME
    result = _list['[1]/tags']
    n0print(f"assert7 = {result}")
    assert7 = ["user", "passive2"]
    assert json.dumps(result, sort_keys=True) == json.dumps(assert7, sort_keys=True)

    _list['1/tags/[1]'] = 'passive3'
    result = _list['[1]/tags']
    n0print(f"assert8 = {result}")
    assert8 = ["user", "passive3"]
    assert json.dumps(result, sort_keys=True) == json.dumps(assert8, sort_keys=True)

    # _list['1/tags/1'] = 'passive4'  # FIXME!!!
    # result = _list['[1]/tags']
    # n0print(f"assert9 = \"{result}\"")
    # assert9 = ["user", "passive4"]
    # assert json.dumps(result, sort_keys=True) == json.dumps(assert9, sort_keys=True)

    test_data = {
        'users': [
            {'name': 'John', 'tags': 'admin'},
            {'name': 'Jane', 'tags': ['user', 'active']}
        ],
        'config': {
            'theme': 'dark',
            'features': {'notifications': True}
        }
    }
    _dict = n1dict(test_data)
    n0debug("_dict")

    n0print(_dict.to_json())
    n0print(_dict.to_xml())
    n0print(_dict.to_xpath())

    _dict.to_scalar('/missing_item')
    n0debug("_dict['/missing_item']")

    n0print("1. Testing append_to_path:")
    _dict.append_to_path('users[0]/tags', 'moderator0')
    _dict.append_to_path('/users[0]/tags', 'moderator1')
    _dict.append_to_path('/users[0]/tags', 'moderator1')
    _dict.append_to_path('/users/[0]/tags', 'moderator2')
    _dict.append_to_path('/users/tags', 'moderator3')
    n0debug("_dict['users[0]/tags']")
    n0debug("_dict['/users[0]/tags']")
    n0debug("_dict['/users/[0]/tags']")
    n0debug("_dict['/users/tags']")

    n0print("2. Testing to_list:")
    n0debug("_dict['/config/theme']")
    _dict.to_list('/config/theme')
    n0debug("_dict['/config/theme']")
    _dict.to_list('/nonexistent')
    n0debug("_dict['/nonexistent']")

    n0print("3. Testing to_scalar:")
    n0debug_calc(_dict.get('/single_item'))
    _dict['/single_item'] = ['only_one']
    n0debug("_dict['/single_item']")
    _dict.to_scalar('/single_item')
    n0debug("_dict['/single_item']")
    _dict.to_scalar('/missing_item')
    n0debug("_dict['/missing_item']")

    n0print("4. Testing extend_path:")
    n0debug("_dict['/config/theme']")
    _dict.extend_path('/config/theme', ['light', 'auto'])
    n0debug("_dict['/config/theme']")
    _dict['/config/theme'].extend(['light2', 'auto2'])
    n0debug("_dict['/config/theme']")

    n0print("5. Testing method chaining:")
    result = (
        _dict.chain()
            .set('/workflow/step1', 'initial')
            .to_list('/workflow/step1')
            .append('/workflow/step1', 'second')
            .append('/workflow/step1', 'third')
            .done()
    )
    n0debug("result['/workflow/step1']")

    n0print("6. Complex transformation workflow:")
    workflow_structure = n1dict({'data': 'start'})
    n0debug("workflow_structure['/data']")
    workflow_structure.append_to_path('/data', 'middle')
    n0debug("workflow_structure['/data']")
    workflow_structure.extend_path('/data', ['end1', 'end2'])
    n0debug("workflow_structure['/data']")

    # Create a single-item list to test scalar conversion
    workflow_structure['/single'] = ['lone_item']
    n0debug("workflow_structure['/single']")
    workflow_structure.to_scalar('/single')
    n0debug("workflow_structure['/single']")

    n0print(f"7. Final state:")
    n0debug("_dict")


# ******************************************************************************
def main():
    test_n1dict_n1list()
# ******************************************************************************

if __name__ == '__main__':
    init_logger(debug_timeformat=None)
    main()
    n0print("Mission acomplished")


################################################################################
__all__ = (
    'test_n1dict_n1list',
    'main',
)
################################################################################

