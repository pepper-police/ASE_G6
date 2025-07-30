#!/bin/bash

# おまじない
set -e
echo "set up"
sudo apt update
sudo apt install python3 python3-venv python3-pip

# venvの作成
if [ ! -d "venv" ]; then
    echo "creating virtual env..."
    python3 -m venv venv
else
    echo "'venv' already exists"
fi

# venvの有効化
echo "activate virtual env..."
source venv/bin/activate

# 必要物のインストール
echo "Installing ..."
pip install opencv-python imagezmq

echo 'Done'