#!/bin/bash

# おまじない
set -e
echo "set up"
sudo apt update
# sudo apt install python3 python3-venv pip3 -y
# OpenCVとimagezmqのインストール
pip3 install opencv-python
pip3 install imagezmq
