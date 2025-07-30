# Raspberry Pi のセットアップ手順

### OS の変更
Ubuntu 24.04 を採用する

### リポジトリのクローン
```bash
git clone https://github.com/pepper-police/ASE_G6
```

### セットアップスクリプトの実行
```bash
bash setup_raspi.sh
```

### VPN の設定
詳細は別ドキュメントを参照

設定した ip アドレスと研究室名 (Raspberry Pi 識別名) を `send_stream.py` に反映

### 運用例
```bash
screen -S sender
python3 send_stream.py
(Ctrl-a - d)
```