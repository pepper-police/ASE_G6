#!/bin/bash

set -e
echo "setup YOLO env"
sudo apt update
sudo apt install libgl1 python3 python3-venv python3-pip -y

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

# ultralyticsのインストール
echo "Installing ultralytics..."
pip install ultralytics opencv-python zmq imagezmq lap

echo 'Done'
