@echo off
set "fromdir=%1"
if "%fromdir%"=="" set "fromdir=%~dp0"

echo fromdir=%fromdir%
call :seek_and_destroy  .pytest_cache\v\cache "nodeids,stepwise,lastfailed"
call :seek_and_destroy  .pytest_cache\v
call :seek_and_destroy  .pytest_cache ".gitignore,CACHEDIR.TAG,README.md"
call :seek_and_destroy  __pycache__ .pyc
call :seek_and_destroy  n0struct\test "test.tmp"

echo THE END
goto :eof

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:seek_and_destroy <dir name in %fromdir%> <file masks to delete in dir path/subpath>
:: Looking for directories <%1> in <%fromdir%>
:: %1 = dir name in %fromdir%
:: %2 = file masks to delete in dir path/subpath
for /f "tokens=*" %%i in ('cmd.exe /c dir /s /b /a:d "%fromdir%"') do (
    REM echo "### %%i
    REM echo "%%~nxi"=="%~1"
    REM if "%%~nxi"=="%~1" call :find_and_clear "%%i" "%~2"
    call :endswith result "%%i" "%~1"
    REM echo result: "%%i" == "%~1" = %result22% ###????
    if defined result call :find_and_clear "%%i" "%~2"
) 
goto :eof
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:find_and_clear <dir path> <file masks to delete in dir path/subpath>
:: Looking for files <%2> in <%1>
:: %1 = dir path to find_and_clear
:: %2 = file masks to delete in dir path/subpath
echo ***FOUND DIR*** %~1
REM echo ***LOOKING FOR EXT*** %~2
:: Parse elem1,elem2,elemN
for %%i in (%~2) do (
    REM echo ===SEARCH FOR EXT=== %%i
    if "%%i"=="" echo FATAL ERROR: extention is empty after parsing "%~2"&&exit
    REM echo 'cmd.exe /c dir /s /b /a:-d "%~1\*%%i"'
    for /f "tokens=*" %%j in ('cmd.exe /c dir /s /b /a:-d "%~1\*%%i" 2^> nul') do (
        if "%%j"=="" echo FATAL ERROR: file name is empty after search ""%~1\*%%i""&&exit
        REM echo ---FOUND FILE--- %%j
        REM if "%%~nxj"=="%%~nxj" call :find_and_clear "%i" "%~2"
        call :endswith result "%%j" "%%i"
        REM echo result: "%%j" == "%%i" = %result%
        if not defined result echo FATAL ERROR: name of found file "%%j" not ends with "%%i"&&exit
        echo --- del "%%j"
        del "%%j"
    ) 
)
echo --- rmdir "%~1"
rmdir "%~1"
goto :eof
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:endswith <resultVar> <stringVar> <stringTail>
:: %1 = resultVar
:: %2 = stringVar
:: %2 = stringTail
REM echo result=1=%result%
call :strlen tmp_tail_len "%~3"
REM echo tmp_tail_len=%tmp_tail_len%
call :ends tmp_tail "%~2" %tmp_tail_len%
REM echo tmp_tail  =%tmp_tail%
REM echo check_tail=%~3
set "%~1="
setlocal EnableDelayedExpansion
REM echo tmp_result=0=!tmp_result!
if "%tmp_tail%"=="%~3" set "tmp_result=TRUE"
REM echo tmp_result=1=!tmp_result!
endlocal&&set "%~1=%tmp_result%"
REM echo tmp_result=2=%tmp_result%
REM echo result=2=%result%
goto :eof
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:ends <resultVar> <stringVar> <lenght from the end>
:: %1 = resultVar
:: %2 = stringVar
:: %3 = lenght from the end
set "tmp1=%~2"
setlocal EnableDelayedExpansion
set "tmp2=!tmp1:~-%3!"
endlocal&&set "%~1=%tmp2%"
goto :eof
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:strlen <resultVar> <stringVar>
:: %1 = resultVar
:: %2 = stringVar
set "tmp=%~2"
setlocal EnableDelayedExpansion
set "len=0"
if defined tmp (
    set "len=1"
    for %%P in (4096 2048 1024 512 256 128 64 32 16 8 4 2 1) do (
        if "!tmp:~%%P,1!" NEQ "" ( 
            set /a "len+=%%P"
            set "tmp=!tmp:~%%P!"
        )
    )
)    
endlocal&&set "%~1=%len%"
goto :eof
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
