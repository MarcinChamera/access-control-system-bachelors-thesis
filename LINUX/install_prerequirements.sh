#!/bin/bash
sudo apt --yes install python3.7
cd ..
python3.7 get-pip.py
sudo apt --yes install python3.7-venv
python3.7 -m venv env
source env/bin/activate
python3.7 -m pip install --upgrade pip
python3.7 -m pip install -r requirements.txt
sudo apt-get install python3.7-tk
deactivate
