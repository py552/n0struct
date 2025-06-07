import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")

from n0struct import *
import json

def test_n0compare():
    dict1 = {
        'tranzations': [
            {'date': "11/01/2025", 'authcode': "00000001", 'amount': 10, 'currency': "USD"},
            {'date': "12/01/2025", 'authcode': "00000002", 'amount': 11, 'currency': "EUR"},
            {'date': "13/01/2025", 'authcode': "00000003", 'amount': 12, 'currency': "GBP"},
            {'date': "14/01/2025", 'authcode': "00000004", 'amount': 13, 'currency': "AED"},
            {'date': "15/01/2025", 'authcode': "00000005", 'amount': 14, 'currency': "SAR"},
        ]
    }
    result = n0compare(dict1, dict1)
    # print(f"assert1 = {json.dumps(result, sort_keys=True)}")
    n0print(f"assert1 = {n0dict(result).to_json()}")

    assert1 = {
        "only_in_1": [  ],
        "only_in_2": [  ],
        "diffs": {  }
    }
    assert json.dumps(result, sort_keys=True) == json.dumps(assert1, sort_keys=True)

    dict2 = {
        'tranzations': [
            {'date': "11/01/2025", 'authcode': "10000001", 'amount': 10, 'currency': "USD"},
            {'date': "12/01/2025", 'authcode': "10000002", 'amount': 11, 'currency': "EUR"},
            {'date': "13/01/2025", 'authcode': "10000003", 'amount': 12, 'currency': "GBP"},
            {'date': "14/01/2025", 'authcode': "10000004", 'amount': 13, 'currency': "AED"},
            {'date': "15/01/2025", 'authcode': "10000005", 'amount': 14, 'currency': "SAR"},
        ]
    }
    result = n0compare(dict1, dict2)
    # print(f"assert2 = {json.dumps(result, sort_keys=True)}")
    n0print(f"assert2 = {n0dict(result).to_json()}")
    assert2 = {
        "only_in_1": [  ],
        "only_in_2": [  ],
        "diffs": {
            "/tranzations[0]/authcode": [ "00000001", [ "/tranzations[0]/authcode", "10000001" ] ],
            "/tranzations[1]/authcode": [ "00000002", [ "/tranzations[1]/authcode", "10000002" ] ],
            "/tranzations[2]/authcode": [ "00000003", [ "/tranzations[2]/authcode", "10000003" ] ],
            "/tranzations[3]/authcode": [ "00000004", [ "/tranzations[3]/authcode", "10000004" ] ],
            "/tranzations[4]/authcode": [ "00000005", [ "/tranzations[4]/authcode", "10000005" ] ]
        }
    }
    assert json.dumps(result, sort_keys=True) == json.dumps(assert2, sort_keys=True)

    result = n0compare(dict1['tranzations'], dict2['tranzations'])
    # print(f"assert3 = {json.dumps(result, sort_keys=True)}")
    n0print(f"assert3 = {n0dict(result).to_json()}")
    assert3 = {
        "only_in_1": [  ],
        "only_in_2": [  ],
        "diffs": {
            "[0]/authcode": [ "00000001", [ "[0]/authcode", "10000001" ] ],
            "[1]/authcode": [ "00000002", [ "[1]/authcode", "10000002" ] ],
            "[2]/authcode": [ "00000003", [ "[2]/authcode", "10000003" ] ],
            "[3]/authcode": [ "00000004", [ "[3]/authcode", "10000004" ] ],
            "[4]/authcode": [ "00000005", [ "[4]/authcode", "10000005" ] ]
        }
    }
    assert json.dumps(result, sort_keys=True) == json.dumps(assert3, sort_keys=True)

    transform_xpaths = {
        re.compile(r"/tranzations\[\d+]/authcode"): [lambda obj: _EXCLUDE_NODE_MARKER],
    }
    result = n0compare(transform_structure(dict1, transform_xpaths), transform_structure(dict2, transform_xpaths))
    # print(f"assert4 = {json.dumps(result, sort_keys=True)}")
    n0print(f"assert4 = {n0dict(result).to_json()}")
    assert json.dumps(result, sort_keys=True) == json.dumps(assert1, sort_keys=True)

    dict2 = {
        'tranzations': [
            {'date': "11/01/2025", 'authcode': "00000001", 'amount': 10, 'currency': "USD"},
            {'date': "13/01/2025", 'authcode': "00000003", 'amount': 12, 'currency': "GBP"},
            {'date': "13/01/2025", 'authcode': "00000003", 'amount': 12, 'currency': "GBP"},
            {'date': "14/01/2025", 'authcode': "00000004", 'amount': 13, 'currency': "AED"},
            {'date': "15/01/2025", 'authcode': "20000005", 'amount': 14, 'currency': "SAR"},
            {'date': "16/01/2025", 'authcode': "00000006", 'amount': 15, 'currency': "JPY"},
        ]
    }
    result = n0compare(dict1, dict2)
    # print(f"assert5 = {json.dumps(result, sort_keys=True)}")
    n0print(f"assert5 = {n0dict(result).to_json()}")
    assert5 = {
        "only_in_1": [  ],
        "only_in_2": [ "/tranzations[5]" ],
        "diffs": {
            "/tranzations[1]/currency": [ "EUR",        [ "/tranzations[2]/currency", "GBP"        ] ],
            "/tranzations[1]/date":     [ "12/01/2025", [ "/tranzations[2]/date",     "13/01/2025" ] ],
            "/tranzations[1]/amount":   [ 11,           [ "/tranzations[2]/amount",   12           ] ],
            "/tranzations[1]/authcode": [ "00000002",   [ "/tranzations[2]/authcode", "00000003"   ] ],
            "/tranzations[4]/authcode": [ "00000005",   [ "/tranzations[4]/authcode", "20000005"   ] ]
        }
    }
    assert json.dumps(result, sort_keys=True) == json.dumps(assert5, sort_keys=True)

    result = n0compare(dict1, dict2, fuzzy_threshold = 4)
    # print(f"assert6 = {json.dumps(result, sort_keys=True)}")
    n0print(f"assert6 = {n0dict(result).to_json()}")
    assert6 = {
        "only_in_1": [ "/tranzations[1]" ],
        "only_in_2": [ "/tranzations[2]", "/tranzations[5]" ],
        "diffs": {
            "/tranzations[4]/authcode": [ "00000005",   [ "/tranzations[4]/authcode", "20000005"   ] ]
        }
    }
    assert json.dumps(result, sort_keys=True) == json.dumps(assert6, sort_keys=True)

# ******************************************************************************
def main():
    test_n0compare()
# ******************************************************************************

if __name__ == '__main__':
    init_logger(debug_timeformat=None)
    main()
    n0print("Mission acomplished")

################################################################################
__all__ = (
    'test_n0compare',
    'main',
)
################################################################################

