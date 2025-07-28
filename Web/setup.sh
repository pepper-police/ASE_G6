#!/bin/bash

set -e

echo "=== Apache2 インストール ==="
sudo apt update
sudo apt install -y apache2

echo "=== Python3 と CGI有効化 ==="
sudo apt install -y python3 python3-pip
sudo a2enmod cgi
sudo systemctl restart apache2

echo "=== ディレクトリ構成作成 ==="
WEB_DIR="/var/www/html/lab_visitors"
sudo mkdir -p "$WEB_DIR/images"
sudo mkdir -p "$WEB_DIR/cgi-bin"

echo "=== HTML/JS/CSS 配置 ==="
# 例: 現在のディレクトリに index.html, script.js, images/ があるとする
sudo cp index.html "$WEB_DIR/"
sudo cp script.js "$WEB_DIR/"
sudo cp -r images "$WEB_DIR/"

echo "=== CGIスクリプト配置 ==="
# make_list.py は JSON を返すスクリプト
sudo cp make_list.py "$WEB_DIR/cgi-bin/"
sudo chmod 755 "$WEB_DIR/cgi-bin/make_list.py"

echo "=== Apache設定変更（lab_visitors用） ==="

# 設定ファイル作成（lab_visitors.conf）
CONF_PATH="/etc/apache2/sites-available/lab_visitors.conf"
sudo tee "$CONF_PATH" > /dev/null <<EOF
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot $WEB_DIR

    <Directory "$WEB_DIR">
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>

    ScriptAlias /make_list.py "$WEB_DIR/cgi-bin/make_list.py"
    <Directory "$WEB_DIR/cgi-bin">
        Options +ExecCGI
        AddHandler cgi-script .py
        Require all granted
    </Directory>

    ErrorLog \${APACHE_LOG_DIR}/lab_visitors_error.log
    CustomLog \${APACHE_LOG_DIR}/lab_visitors_access.log combined
</VirtualHost>
EOF

echo "=== Apache設定有効化と再起動 ==="
sudo a2dissite 000-default.conf
sudo a2ensite lab_visitors.conf
sudo systemctl reload apache2

echo "=== 完了！ http://<サーバーIP>/ にアクセスしてください ==="
