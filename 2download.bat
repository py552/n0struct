@echo off
set TEST_MODE=TRUE
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Determine directory/project name
set "mydir=%~dp0"
set "mydir=%mydir:~0,-1%"
for /f %%i in ("%mydir%") do set "mydir=%%~ni"
for /f %%i in ('setup.py --name') do set "myprj=%%i"
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Check/create virtual environment
set "venv_dir=..\%mydir%.virtenv"
if not exist %venv_dir% (
    echo **********************************************************************
    echo *** venv %venv_dir%
    echo **********************************************************************
    python -m venv %venv_dir%
    call %venv_dir%\Scripts\activate.bat
    python -m pip install pytest
)
call %venv_dir%\Scripts\activate.bat
pushd %venv_dir%
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
echo **********************************************************************
echo *** pip show %myprj%
echo **********************************************************************
python -m pip show %myprj%
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
:: Download
if not "%TEST_MODE%"=="" (
    set "test_dnload=-i https://test.pypi.org/simple/"
    set "test_upload=--repository testpypi"
rem Because of not all required packages are in test repository,
rem we need to install them from the main
    python -m pip install --upgrade xmltodict
)
echo **********************************************************************
echo *** pip install --upgrade %test_dnload% %myprj%
echo **********************************************************************
python -m pip install --upgrade %test_dnload% %myprj%
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
echo **********************************************************************
echo *** pip show %myprj%
echo **********************************************************************
python -m pip show %myprj%
echo **********************************************************************
echo *** pytest --pyargs %myprj%
echo **********************************************************************
pytest --pyargs %myprj%
::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
popd
