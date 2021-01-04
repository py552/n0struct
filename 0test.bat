echo **********************************************************************
echo *** pytest
echo **********************************************************************
python -m pytest
if not "%errorlevel%"=="0" echo ERROR with autotests!&&exit 