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
    load_ini,
    save_file,
    load_file,
    load_csv,
    load_lines,
    init_logger,
)
init_logger(debug_timeformat = None, debug_show_object_id = False, debug_logtofile = False)

# ******************************************************************************
def test_files_processing():
    test_ini_path = os.path.join(mydir, "test.ini")
    n0debug("test_ini_path")

    test_ini = load_ini(test_ini_path)
    n0debug("test_ini")

    tmp_file = os.path.join(mydir, "test.tmp")
    save_file(tmp_file, test_ini, mode='wb', EOL='\n')

    test_ini = load_ini(tmp_file)
    os.unlink(tmp_file)
    n0debug_calc(test_ini, "test_ini(after save)")

    # n0debug_calc( 'AAA\n'  .rstrip( '\r\n').encode(),     r"'AAA\n'  .rstip('\r\n')")
    # n0debug_calc( 'AAA\r\n'.rstrip( '\r\n').encode(),     r"'AAA\r\n'.rstip('\r\n')")
    # n0debug_calc( 'AAA\r'  .rstrip( '\r\n').encode(),     r"'AAA\r'  .rstip('\r\n')")
    # n0debug_calc( 'AAA\n\r'.rstrip( '\r\n').encode(),     r"'AAA\n\r'.rstip('\r\n')")
    # n0debug_calc(b'BBB\n'  .rstrip(b'\r\n')         ,     r"b'BBB\n'  .rstip(b'\r\n')")
    # n0debug_calc(b'BBB\r\n'.rstrip(b'\r\n')         ,     r"b'BBB\r\n'.rstip(b'\r\n')")
    # n0debug_calc(b'BBB\r'  .rstrip(b'\r\n')         ,     r"b'BBB\r'  .rstip(b'\r\n')")
    # n0debug_calc(b'BBB\n\r'.rstrip(b'\r\n')         ,     r"b'BBB\n\r'.rstip(b'\r\n')")

    # removed walrus operator for compatibility with 3.7

    tmp_file_CRLF = os.path.join(mydir, "CRLF.csv")
    output_buffer = b'A,B,C\r\n1,2,3\r\n4,5,6\r\n'
    save_file(tmp_file_CRLF,    output_buffer, mode='wb')
    assert output_buffer == load_file(tmp_file_CRLF, read_mode='b')

    tmp_file_CRLF2 = os.path.join(mydir, "CRLF2.csv")
    output_buffer = b'A,B,C\r\n1,2,3\r\n4,5,6'
    save_file(tmp_file_CRLF2,   output_buffer, mode='wb')
    assert output_buffer == load_file(tmp_file_CRLF2, read_mode='b')

    tmp_file_LF = os.path.join(mydir, "LF.csv")
    output_buffer = b'A,B,C\n1,2,3\n4,5,6\n'
    save_file(tmp_file_LF,      output_buffer, mode='wb')
    assert output_buffer == load_file(tmp_file_LF, read_mode='b')

    tmp_file_LF2 = os.path.join(mydir, "LF2.csv")
    output_buffer = b'A,B,C\n1,2,3\n4,5,6'
    save_file(tmp_file_LF2,     output_buffer, mode='wb')
    assert output_buffer == load_file(tmp_file_LF2, read_mode='b')

    tmp_file_CR = os.path.join(mydir, "CR.csv")
    output_buffer = b'A,B,C\r1,2,3\r4,5,6\r'
    save_file(tmp_file_CR,      output_buffer, mode='wb')
    assert output_buffer == load_file(tmp_file_CR, read_mode='b')

    tmp_file_CR2 = os.path.join(mydir, "CR2.csv")
    output_buffer = b'A,B,C\r1,2,3\r4,5,6'
    save_file(tmp_file_CR2,     output_buffer, mode='wb')
    assert output_buffer == load_file(tmp_file_CR2, read_mode='b')

    tmp_file_LFCR = os.path.join(mydir, "LFCR.csv")
    output_buffer = b'A,B,C\n\r1,2,3\n\r4,5,6\n\r'
    save_file(tmp_file_LFCR,    output_buffer, mode='wb')
    assert output_buffer == load_file(tmp_file_LFCR, read_mode='b')

    tmp_file_LFCR2 = os.path.join(mydir, "LFCR2.csv")
    output_buffer = b'A,B,C\n\r1,2,3\n\r4,5,6'
    save_file(tmp_file_LFCR2, output_buffer, mode='wb')
    assert output_buffer == load_file(tmp_file_LFCR2, read_mode='b')

    n0debug_calc(load_file(tmp_file_CRLF).encode('utf-8'),                  "CRLF                    read_mode='t'")
    n0debug_calc(load_file(tmp_file_CRLF, read_mode='b'),                   "CRLF                    read_mode='b'")
    n0debug_calc(list(load_lines(tmp_file_CRLF)),                           "CRLFlines               read_mode='t'")
    n0debug_calc(list(load_lines(tmp_file_CRLF)),                           "CRLFlines               read_mode='b'")
    n0debug_calc(list(load_csv(tmp_file_CRLF)),                             "CRLFcsv                 read_mode='t'")
    n0debug_calc(list(load_csv(tmp_file_CRLF, read_mode='b')),              "CRLFcsv                 read_mode='b'")

    n0debug_calc(load_file(tmp_file_CRLF2).encode('utf-8'),                 "CRLF(wo last CRLF)      read_mode='t'")
    n0debug_calc(load_file(tmp_file_CRLF2, read_mode='b'),                  "CRLF(wo last CRLF)      read_mode='b'")
    n0debug_calc(list(load_lines(tmp_file_CRLF2)),                          "CRLF(wo last CRLF)lines read_mode='t'")
    n0debug_calc(list(load_lines(tmp_file_CRLF2)),                          "CRLF(wo last CRLF)lines read_mode='b'")
    n0debug_calc(list(load_csv(tmp_file_CRLF2)),                            "CRLF(wo last CRLF)csv   read_mode='t'")
    n0debug_calc(list(load_csv(tmp_file_CRLF2, read_mode='b')),             "CRLF(wo last CRLF)csv   read_mode='b'")

    n0debug_calc(load_file(tmp_file_LF).encode('utf-8'),                    "LF                      read_mode='t'")
    n0debug_calc(load_file(tmp_file_LF, read_mode='b'),                     "LF                      read_mode='b'")
    n0debug_calc(list(load_lines(tmp_file_LF)),                             "LFlines                 read_mode='t'")
    n0debug_calc(list(load_lines(tmp_file_LF)),                             "LFlines                 read_mode='b'")
    n0debug_calc(list(load_csv(tmp_file_LF)),                               "LFcsv                   read_mode='t'")
    n0debug_calc(list(load_csv(tmp_file_LF, read_mode='b')),                "LFcsv                   read_mode='b'")

    n0debug_calc(load_file(tmp_file_LF2).encode('utf-8'),                   "LF(wo last CRLF)        read_mode='t'")
    n0debug_calc(load_file(tmp_file_LF2, read_mode='b'),                    "LF(wo last CRLF)        read_mode='b'")
    n0debug_calc(list(load_lines(tmp_file_LF2)),                            "LF(wo last CRLF)lines   read_mode='t'")
    n0debug_calc(list(load_lines(tmp_file_LF2)),                            "LF(wo last CRLF)lines   read_mode='b'")
    n0debug_calc(list(load_csv(tmp_file_LF2)),                              "LF(wo last CRLF)csv     read_mode='t'")
    n0debug_calc(list(load_csv(tmp_file_LF2, read_mode='b')),               "LF(wo last CRLF)csv     read_mode='b'")

    n0debug_calc(load_file(tmp_file_CR).encode('utf-8'),                    "CR                      read_mode='t'")
    n0debug_calc(load_file(tmp_file_CR, read_mode='b'),                     "CR                      read_mode='b'")
    n0debug_calc(list(load_lines(tmp_file_CR)),                             "CRlines                 read_mode='t'")
    n0debug_calc(list(load_lines(tmp_file_CR)),                             "CRlines                 read_mode='b'")
    n0debug_calc(list(load_csv(tmp_file_CR)),                               "CRcsv                   read_mode='t'")
    n0debug_calc(list(load_csv(tmp_file_CR, read_mode='b')),                "CRcsv                   read_mode='b'")
    n0debug_calc(list(load_csv(tmp_file_CR, read_mode='b', EOL='\r')),      "CRcsv                   read_mode='b' EOL='\\r'")

    n0debug_calc(load_file(tmp_file_CR2).encode('utf-8'),                   "CR(wo last CRLF)        read_mode='t'")
    n0debug_calc(load_file(tmp_file_CR2, read_mode='b'),                    "CR(wo last CRLF)        read_mode='b'")
    n0debug_calc(list(load_lines(tmp_file_CR2)),                            "CR(wo last CRLF)lines   read_mode='t'")
    n0debug_calc(list(load_lines(tmp_file_CR2)),                            "CR(wo last CRLF)lines   read_mode='b'")
    n0debug_calc(list(load_csv(tmp_file_CR2)),                              "CR(wo last CRLF)csv     read_mode='t'")
    n0debug_calc(list(load_csv(tmp_file_CR2, read_mode='b')),               "CR(wo last CRLF)csv     read_mode='b'")
    n0debug_calc(list(load_csv(tmp_file_CR2, read_mode='b', EOL='\r')),     "CR(wo last CRLF)csv     read_mode='b' EOL='\\r'")

    n0debug_calc(load_file(tmp_file_LFCR).encode('utf-8'),                  "LFCR                    read_mode='t'")
    n0debug_calc(load_file(tmp_file_LFCR, read_mode='b'),                   "LFCR                    read_mode='b'")
    n0debug_calc(list(load_lines(tmp_file_LFCR)),                           "LFCRlines               read_mode='t'")
    n0debug_calc(list(load_lines(tmp_file_LFCR)),                           "LFCRlines               read_mode='b'")
    n0debug_calc(list(load_csv(tmp_file_LFCR)),                             "LFCRcsv                 read_mode='t'")
    n0debug_calc(list(load_csv(tmp_file_LFCR, read_mode='b')),              "LFCRcsv                 read_mode='b'")
    n0debug_calc(list(load_csv(tmp_file_LFCR, read_mode='b', EOL='\n\r')),  "LFCRcsv                 read_mode='b' EOL='\\n\\r'")

    n0debug_calc(load_file(tmp_file_LFCR2).encode('utf-8'),                 "LFCR(wo last CRLF)      read_mode='t'")
    n0debug_calc(load_file(tmp_file_LFCR2, read_mode='b'),                  "LFCR(wo last CRLF)      read_mode='b'")
    n0debug_calc(list(load_lines(tmp_file_LFCR2)),                          "LFCR(wo last CRLF)lines read_mode='t'")
    n0debug_calc(list(load_lines(tmp_file_LFCR2)),                          "LFCR(wo last CRLF)lines read_mode='b'")
    n0debug_calc(list(load_csv(tmp_file_LFCR2)),                            "LFCR(wo last CRLF)csv   read_mode='t'")
    n0debug_calc(list(load_csv(tmp_file_LFCR2, read_mode='b')),             "LFCR(wo last CRLF)csv   read_mode='b'")
    n0debug_calc(list(load_csv(tmp_file_LFCR2, read_mode='b', EOL='\n\r')), "LFCR(wo last CRLF)csv   read_mode='b' EOL='\\n\\r'")

    os.unlink(tmp_file_CRLF)
    os.unlink(tmp_file_CRLF2)
    os.unlink(tmp_file_LF)
    os.unlink(tmp_file_LF2)
    os.unlink(tmp_file_CR)
    os.unlink(tmp_file_CR2)
    os.unlink(tmp_file_LFCR)
    os.unlink(tmp_file_LFCR2)

# ******************************************************************************
def main():
    test_files_processing()
# ******************************************************************************

if __name__ == '__main__':
    main()
    n0print("Mission acomplished")


################################################################################
__all__ = (
    'test_files_processing',
    'main',
    'mydir',
)
################################################################################
