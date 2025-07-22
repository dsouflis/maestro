@echo off
:: Run from ANY folder (adjust path if needed)
pushd "%~dp0"
call "venv\Scripts\activate.bat"
python "src\main.py" %*
call "venv\Scripts\deactivate.bat"
popd
