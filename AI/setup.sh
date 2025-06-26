#!/bin/bash

set -e

echo "setup YOLO env"

# Python3のインストール確認とインストール
if ! type python3 &> /dev/null
then
    echo "'python3' not found, install 'python3'..."
    sudo apt update
    sudo apt install -y python3
else
    echo "'Python3' found"
fi

# pipのインストール確認とインストール
if ! type pip3 &> /dev/null
then
    echo "'pip3' not found, install 'pip3'..."
    sudo apt install -y python3-pip
else
    echo "'pip3' found"
fi

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