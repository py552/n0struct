@echo off

set "TMP_FILE=%~dp0\$tmp$"

grep -E "^(def|class)\W+(.+)?\(.*$" "%~1" ^
    | perl -pE "s/^(def|class)\W+(.+)?\(.*$/\x20\x20\x20\x20'\2'\x2C/g" ^
    > "%TMP_FILE%1"

grep -E "^([a-zA-Z]\w*)\s*=\s*.*$" "%~1" ^
    | perl -pE "s/^([a-zA-Z]\w*)\s*=\s*.*$/\x20\x20\x20\x20'\1'\x2C/g" ^
    >> "%TMP_FILE%1"

call :is_file_empty "%TMP_FILE%1"
if ERRORLEVEL 1 goto :file_is_empty

echo *** FOUND
REM timeout /T 10

perl -pE "s/\r?\n/\r/g" "%~1" | perl -pE "s/(#{80}\r)?__all__ = \(\r( {4}.*?\,\r)+\)\r\#{80}\r//g" | perl -pE "s/\r/\r\n/g">"%TMP_FILE%2"

echo ################################################################################>> "%TMP_FILE%2"
echo __all__ = (>> "%TMP_FILE%2"
copy /b "%TMP_FILE%2" + "%TMP_FILE%1" "%TMP_FILE%2">nul
echo )>> "%TMP_FILE%2"
echo ################################################################################>> "%TMP_FILE%2"

@echo on
move "%~1" "%~1.bak"
move "%TMP_FILE%2" "%~1"

@REM timeout /T 10

:file_is_empty
del "%TMP_FILE%1">nul
@echo off
goto :eof

:is_file_empty
if "%~z1" == "0" exit /b 1
exit /b 0
goto :eof
