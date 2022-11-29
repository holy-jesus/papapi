#!/bin/bash

sudo apt update
sudo apt install -y python3 python3-venv python3-pip git
git clone https://github.com/holy-jesus/papapi.git
cd ./papapi/
python3 -m venv ./venv/
source ./venv/bin/activate
pip3 install -r requirements.txt
deactivate
echo Successfully installed! To run the site, type ./run.sh
