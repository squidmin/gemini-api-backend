# !/bin/bash

pyenv local 3.12.0b4
eval "$(pyenv init --path)"
python3 --version
pip3 install -r requirements.txt
