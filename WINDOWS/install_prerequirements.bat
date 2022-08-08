@echo off

:start
cls

py get-pip.py
py -m pip install --user virtualenv
cd ..
py -m venv env
CALL env\Scripts\activate
pip install -r requirements.txt
deactivate
