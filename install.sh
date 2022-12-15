#!/bin/bash

if command -v apt &> /dev/null; then
    sudo apt install -y python3 python3-venv python3-pip git
elif command -v pacman &> /dev/null; then
    sudo pacman -S --noconfirm python3 python3-venv python3-pip git
else
    echo "Your distribution is currently not supported"
    exit
fi
git clone https://github.com/holy-jesus/papapi.git && cd ./papapi/
python3 -m venv ./venv/
source ./venv/bin/activate
pip3 install -r ./papapi/requirements.txt
deactivate
echo Successfully installed! To run the site, type ./run.sh
