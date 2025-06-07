copy nul result.txt
python test_n0struct01.py >> result.txt 2>&1
if ERRORLEVEL 1 exit /b -1
python test_n0struct02.py >> result.txt 2>&1
if ERRORLEVEL 1 exit /b -1
python test_n0struct03.py >> result.txt 2>&1
if ERRORLEVEL 1 exit /b -1
python test_n0struct04.py >> result.txt 2>&1
if ERRORLEVEL 1 exit /b -1
python test_n0struct05.py >> result.txt 2>&1
if ERRORLEVEL 1 exit /b -1
::python test_n0struct06.py >> result.txt 2>&1
::if ERRORLEVEL 1 exit /b -1
python test_n0struct07.py >> result.txt 2>&1
if ERRORLEVEL 1 exit /b -1
python test_n0struct08.py >> result.txt 2>&1
if ERRORLEVEL 1 exit /b -1
python test_n0struct09.py >> result.txt 2>&1
if ERRORLEVEL 1 exit /b -1
python test_n0struct10.py >> result.txt 2>&1
if ERRORLEVEL 1 exit /b -1
python test_n0struct11.py >> result.txt 2>&1
if ERRORLEVEL 1 exit /b -1
python test_n0struct12.py >> result.txt 2>&1
if ERRORLEVEL 1 exit /b -1
