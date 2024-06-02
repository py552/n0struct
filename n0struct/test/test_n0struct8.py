import os
import sys
mydir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, mydir)
sys.path.insert(0, mydir+"/../")
sys.path.insert(0, mydir+"/../../")

from n0struct import (
    save_file,
    load_file,
    n0info,
    n0print,
    n0debug,
    n0debug_calc,
    init_logger,
)


def test_save_load_file():
    test_dict = {"A":"1","B":"2","C":"3"}
    test_str_list = ["StrLine1", "StrLine2", "StrLine3"]
    test_bin_list = [b"BinLine1", b"BinLine2", b"BinLine3"]
    test_str = "StrLine1\nStrLine2\nStrLine3"
    test_bin = b"BinLine1\nBinLine2\nBinLine3"


    for mode in ('t', 'b'):
        for optional_linesep, linesep in enumerate((
            'OS_DEFAULT',
            os.linesep,
            '\n',
            '\r',
            '\r\n',
            '\n\r',
            '$\n^',
        )):
            linesep_ = linesep.encode('unicode_escape').decode().replace('\\','-')
            n0print(f"******* {mode} {linesep_}")

            tmp_file = f"test_dict{linesep_}.tmp"
            n0print(f"* {tmp_file}")
            if not optional_linesep:
                linesep = os.linesep
                save_file(tmp_file, test_dict, mode=mode)
            else:
                save_file(tmp_file, test_dict, mode=mode, EOL=linesep)

            expected_bin_result = linesep.encode().join(f'{key}={value}'.encode() for key,value in test_dict.items())
            n0debug("expected_bin_result")
            read_as_bin_result = load_file(tmp_file, read_mode='b')
            n0debug("read_as_bin_result")
            assert read_as_bin_result == expected_bin_result

            expected_txt_result = '\n'.join(f'{key}={value}' for key,value in test_dict.items())
            n0debug_calc(expected_txt_result.encode(), "expected_txt_result")
            if optional_linesep:
                read_as_txt_result = load_file(tmp_file, EOL=linesep)
                n0debug_calc(read_as_txt_result.encode(), "read_as_txt_result")
                assert read_as_txt_result == expected_txt_result
            read_as_txt_result = load_file(tmp_file)
            n0debug_calc(read_as_txt_result.encode(), "read_as_txt_result")
            if optional_linesep >= 5:
                n0info(f'Autoconvert is impossible with not standard EOL {linesep.encode()}')
            else:
                assert read_as_txt_result == expected_txt_result

            os.unlink(tmp_file)

            ########################################################################

            tmp_file = f"test_str_list{linesep_}.tmp"
            n0print(f"* {tmp_file}")
            if not optional_linesep:
                linesep = os.linesep
                save_file(tmp_file, test_str_list, mode=mode)
            else:
                save_file(tmp_file, test_str_list, mode=mode, EOL=linesep)

            expected_bin_result = b''.join((itm.encode()+linesep.encode()) for itm in test_str_list)
            n0debug("expected_bin_result")
            read_as_bin_result = load_file(tmp_file, read_mode='b')
            n0debug("read_as_bin_result")
            assert read_as_bin_result == expected_bin_result

            expected_txt_result = ''.join(itm+'\n' for itm in test_str_list)
            n0debug_calc(expected_txt_result.encode(), "expected_txt_result")
            if optional_linesep:
                read_as_txt_result = load_file(tmp_file, EOL=linesep)
                n0debug_calc(read_as_txt_result.encode(), "read_as_txt_result")
                assert read_as_txt_result == expected_txt_result
            read_as_txt_result = load_file(tmp_file)
            n0debug_calc(read_as_txt_result.encode(), "read_as_txt_result")
            if optional_linesep >= 5:
                n0info(f'Autoconvert is impossible with not standard EOL {linesep.encode()}')
            else:
                assert read_as_txt_result == expected_txt_result

            os.unlink(tmp_file)

            ########################################################################

            tmp_file = f"test_bin_list{linesep_}.tmp"
            n0print(f"* {tmp_file}")
            if not optional_linesep:
                linesep = os.linesep
                save_file(tmp_file, test_bin_list, mode=mode)
            else:
                save_file(tmp_file, test_bin_list, mode=mode, EOL=linesep)

            expected_bin_result = b''.join((itm+linesep.encode()) for itm in test_bin_list)
            n0debug("expected_bin_result")
            read_as_bin_result = load_file(tmp_file, read_mode='b')
            n0debug("read_as_bin_result")
            assert read_as_bin_result == expected_bin_result
            os.unlink(tmp_file)

            ########################################################################

            tmp_file = f"test_str{linesep_}.tmp"
            n0print(f"* {tmp_file}")
            if not optional_linesep:
                linesep = os.linesep
                save_file(tmp_file, test_str, mode=mode)
            else:
                save_file(tmp_file, test_str, mode=mode, EOL=linesep)

            expected_bin_result = test_str.replace('\n', linesep).encode()
            n0debug("expected_bin_result")
            read_as_bin_result = load_file(tmp_file, read_mode='b')
            n0debug("read_as_bin_result")
            assert read_as_bin_result == expected_bin_result
            os.unlink(tmp_file)

            ########################################################################

            tmp_file = f"test_bin{linesep_}.tmp"
            n0print(f"* {tmp_file}")
            if not optional_linesep:
                linesep = os.linesep
                save_file(tmp_file, test_bin, mode=mode)
            else:
                save_file(tmp_file, test_bin, mode=mode, EOL=linesep)

            expected_bin_result = test_bin
            n0debug("expected_bin_result")
            read_as_bin_result = load_file(tmp_file, read_mode='b')
            n0debug("read_as_bin_result")
            assert read_as_bin_result == expected_bin_result
            os.unlink(tmp_file)

            ########################################################################

# ******************************************************************************
def main():
    test_save_load_file()
# ******************************************************************************

if __name__ == '__main__':
    init_logger(debug_timeformat=None)
    main()
    n0print("Mission acomplished")
