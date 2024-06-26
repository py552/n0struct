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
    save_file(tmp_file:=os.path.join(mydir, "test.tmp"), test_ini, mode='wb', EOL='\n')
    test_ini = load_ini(tmp_file)
    n0debug_calc(test_ini, "test_ini(after save)")

    # n0debug_calc( 'AAA\n'  .rstrip( '\r\n').encode(),     r"'AAA\n'  .rstip('\r\n')")
    # n0debug_calc( 'AAA\r\n'.rstrip( '\r\n').encode(),     r"'AAA\r\n'.rstip('\r\n')")
    # n0debug_calc( 'AAA\r'  .rstrip( '\r\n').encode(),     r"'AAA\r'  .rstip('\r\n')")
    # n0debug_calc( 'AAA\n\r'.rstrip( '\r\n').encode(),     r"'AAA\n\r'.rstip('\r\n')")
    # n0debug_calc(b'BBB\n'  .rstrip(b'\r\n')         ,     r"b'BBB\n'  .rstip(b'\r\n')")
    # n0debug_calc(b'BBB\r\n'.rstrip(b'\r\n')         ,     r"b'BBB\r\n'.rstip(b'\r\n')")
    # n0debug_calc(b'BBB\r'  .rstrip(b'\r\n')         ,     r"b'BBB\r'  .rstip(b'\r\n')")
    # n0debug_calc(b'BBB\n\r'.rstrip(b'\r\n')         ,     r"b'BBB\n\r'.rstip(b'\r\n')")

    n0debug_calc(load_file(os.path.join(mydir,      "CRLF.csv")).encode('utf-8'),               "CRLF       read_mode='t'")
    n0debug_calc(load_file(os.path.join(mydir,      "CRLF.csv"), read_mode='b'),                "CRLF       read_mode='b'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"CRLF.csv"))),                              "CRLFlines  read_mode='t'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"CRLF.csv"))),                              "CRLFlines  read_mode='b'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "CRLF.csv"))),                              "CRLFcsv    read_mode='t'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "CRLF.csv"), read_mode='b')),               "CRLFcsv    read_mode='b'")

    n0debug_calc(load_file(os.path.join(mydir,      "CRLF2.csv")).encode('utf-8'),              "CRLF(wo last CRLF)      read_mode='t'")
    n0debug_calc(load_file(os.path.join(mydir,      "CRLF2.csv"), read_mode='b'),               "CRLF(wo last CRLF)      read_mode='b'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"CRLF2.csv"))),                             "CRLF(wo last CRLF)lines read_mode='t'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"CRLF2.csv"))),                             "CRLF(wo last CRLF)lines read_mode='b'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "CRLF2.csv"))),                             "CRLF(wo last CRLF)csv   read_mode='t'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "CRLF2.csv"), read_mode='b')),              "CRLF(wo last CRLF)csv   read_mode='b'")

    n0debug_calc(load_file(os.path.join(mydir,      "LF.csv")).encode('utf-8'),                 "LF         read_mode='t'")
    n0debug_calc(load_file(os.path.join(mydir,      "LF.csv"), read_mode='b'),                  "LF         read_mode='b'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"LF.csv"))),                                "LFlines    read_mode='t'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"LF.csv"))),                                "LFlines    read_mode='b'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "LF.csv"))),                                "LFcsv      read_mode='t'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "LF.csv"), read_mode='b')),                 "LFcsv      read_mode='b'")

    n0debug_calc(load_file(os.path.join(mydir,      "LF2.csv")).encode('utf-8'),                "LF(wo last CRLF)        read_mode='t'")
    n0debug_calc(load_file(os.path.join(mydir,      "LF2.csv"), read_mode='b'),                 "LF(wo last CRLF)        read_mode='b'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"LF2.csv"))),                               "LF(wo last CRLF)lines   read_mode='t'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"LF2.csv"))),                               "LF(wo last CRLF)lines   read_mode='b'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "LF2.csv"))),                               "LF(wo last CRLF)csv     read_mode='t'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "LF2.csv"), read_mode='b')),                "LF(wo last CRLF)csv     read_mode='b'")

    n0debug_calc(load_file(os.path.join(mydir,      "CR.csv")).encode('utf-8'),                 "CR         read_mode='t'")
    n0debug_calc(load_file(os.path.join(mydir,      "CR.csv"), read_mode='b'),                  "CR         read_mode='b'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"CR.csv"))),                                "CRlines    read_mode='t'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"CR.csv"))),                                "CRlines    read_mode='b'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "CR.csv"))),                                "CRcsv      read_mode='t'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "CR.csv"), read_mode='b')),                 "CRcsv      read_mode='b'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "CR.csv"), read_mode='b', EOL='\r')),       "CRcsv      read_mode='b' EOL='\\r'")

    n0debug_calc(load_file(os.path.join(mydir,      "CR2.csv")).encode('utf-8'),                "CR(wo last CRLF)        read_mode='t'")
    n0debug_calc(load_file(os.path.join(mydir,      "CR2.csv"), read_mode='b'),                 "CR(wo last CRLF)        read_mode='b'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"CR2.csv"))),                               "CR(wo last CRLF)lines   read_mode='t'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"CR2.csv"))),                               "CR(wo last CRLF)lines   read_mode='b'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "CR2.csv"))),                               "CR(wo last CRLF)csv     read_mode='t'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "CR2.csv"), read_mode='b')),                "CR(wo last CRLF)csv     read_mode='b'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "CR2.csv"), read_mode='b', EOL='\r')),      "CR(wo last CRLF)csv     read_mode='b' EOL='\\r'")

    n0debug_calc(load_file(os.path.join(mydir,      "LFCR.csv")).encode('utf-8'),               "LFCR       read_mode='t'")
    n0debug_calc(load_file(os.path.join(mydir,      "LFCR.csv"), read_mode='b'),                "LFCR       read_mode='b'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"LFCR.csv"))),                              "LFCRlines  read_mode='t'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"LFCR.csv"))),                              "LFCRlines  read_mode='b'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "LFCR.csv"))),                              "LFCRcsv    read_mode='t'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "LFCR.csv"), read_mode='b')),               "LFCRcsv    read_mode='b'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "LFCR.csv"), read_mode='b', EOL='\n\r')),   "LFCRcsv    read_mode='b' EOL='\\n\\r'")

    n0debug_calc(load_file(os.path.join(mydir,      "LFCR2.csv")).encode('utf-8'),              "LFCR(wo last CRLF)      read_mode='t'")
    n0debug_calc(load_file(os.path.join(mydir,      "LFCR2.csv"), read_mode='b'),               "LFCR(wo last CRLF)      read_mode='b'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"LFCR2.csv"))),                             "LFCR(wo last CRLF)lines read_mode='t'")
    n0debug_calc(list(load_lines(os.path.join(mydir,"LFCR2.csv"))),                             "LFCR(wo last CRLF)lines read_mode='b'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "LFCR2.csv"))),                             "LFCR(wo last CRLF)csv   read_mode='t'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "LFCR2.csv"), read_mode='b')),              "LFCR(wo last CRLF)csv   read_mode='b'")
    n0debug_calc(list(load_csv(os.path.join(mydir,  "LFCR2.csv"), read_mode='b', EOL='\n\r')),  "LFCR(wo last CRLF)csv   read_mode='b' EOL='\\n\\r'")

    os.unlink(tmp_file)

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
