@echo off
set TEST_MODE=TRUE
REM python -m pip install --upgrade pip
REM python -m pip install --upgrade setuptools wheel
REM python -m pip install twine
REM python -m pip install venv
REM python -m pip install keyring
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Unit testing before building
echo **********************************************************************
echo *** pytest
echo **********************************************************************
python -m pytest
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Determine directory/project name
set "mydir=%~dp0"
set "mydir=%mydir:~0,-1%"
for /f %%i in ("%mydir%") do set "mydir=%%~ni"
for /f %%i in ('setup.py --name') do set "myprj=%%i"
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Increment revision in VERSION
if not exist "VERSION" echo.0.1.-1> VERSION
SetLocal EnableDelayedExpansion 
for /f "eol=; tokens=1,2,3* delims=. " %%i in (VERSION) do (
    set /a next_build=1+%%k
    echo %%i.%%j.%%k -^> %%i.%%j.!next_build!
    echo.%%i.%%j.!next_build!> VERSION
)
SetLocal DisableDelayedExpansion 
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Build distributive
echo **********************************************************************
echo *** setup.py sdist
echo **********************************************************************
call :clean
REM Legacy: source + egg info
REM python setup.py sdist
REM Modern: source + wheel
python setup.py sdist bdist_wheel
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Upload
call :init_credentials
echo **********************************************************************
echo *** twine upload --username %USERNAME% --password XXX %test_upload% dist/*
echo **********************************************************************
python -m twine upload --username %USERNAME% --password %PASSWORD% %test_upload% dist/*
call :clean

echo Mission acomplished
goto :eof
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:clean
:: Safe version ::
if "%fromdir%"=="" set "fromdir=%~dp0"
echo Looking for "%fromdir%\*.pyc"
for /f %%i in ('cmd.exe /c dir /s /b /a:-d "%fromdir%\*.pyc"') do if "%%~xi"==".pyc" (echo *** %%i&&cmd /c del %%i) else (echo SOMETHING WRONG: Try to remove '%%i'&&exit)
echo Looking for "%fromdir%\__pycache__"
for /f %%i in ('cmd.exe /c dir /s /b /a:d "%fromdir%\__pycache__"') do if "%%~ni"=="__pycache__" (echo *** %%i&&cmd /c rmdir %%i) else (echo SOMETHING WRONG: Try to remove '%%i'&&exit)

set "tmp_dir=%fromdir%\.pytest_cache"
if exist "%tmp_dir%" echo *** %tmp_dir%\*.*&&cmd /c rmdir /s /q %tmp_dir%
cmd /c rmdir /s /q .\%myprj%.egg-info\ 2> nul
cmd /c rmdir /s /q .\dist\ 2> nul
cmd /c rmdir /s /q .\build\ 2> nul
goto :eof
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:init_credentials
if not "%TEST_MODE%"=="" (
    set "USERNAME=pythonist552-test"
    set "test_dnload=-i https://test.pypi.org/simple/"
    set "test_upload=--repository testpypi"
) else (
    set "USERNAME=pythonist552"
    set "test_dnload="
    set "test_upload="
)
REM How to save the password into the vault:
REM echo y0uRpA$$w0rD | keyring set pypi %USERNAME%
REM How to retrieve the password from the vault:
REM keyring get pypi %USERNAME%
for /f %%i in ('python -m keyring get pypi %USERNAME%') do set "PASSWORD=%%i"
REM echo PASSWORD=%PASSWORD%
goto :eof
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

