#!/bin/bash

set -e
echo "setup YOLO env"
sudo apt update
sudo apt install python3 python3-venv pip3 -y

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
pip install ultralytics

echo 'Done'