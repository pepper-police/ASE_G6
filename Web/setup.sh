#!/bin/bash

# === Apache2 のインストール ===
echo "Apache2 をインストールします..."
sudo apt update
sudo apt install -y apache2

# === CGI モジュールの有効化 ===
echo "CGI モジュールを有効化します..."
sudo a2enmod cgi

# === ドキュメントルートを /home/ubuntu/web に変更 ===
WEB_DIR="/home/ubuntu/web"
if [ ! -d "$WEB_DIR" ]; then
    echo "Web ディレクトリが存在しません。作成します: $WEB_DIR"
    mkdir -p "$WEB_DIR"
fi

# === サンプル index.html を作成 ===
echo "<h1>Apache is working!</h1>" > "$WEB_DIR/index.html"

# === Apache の設定ファイルを作成 ===
VHOST_CONF="/etc/apache2/sites-available/web.conf"
sudo tee "$VHOST_CONF" > /dev/null <<EOF
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot $WEB_DIR

    <Directory "$WEB_DIR">
        Options +ExecCGI
        AddHandler cgi-script .cgi .py
        AllowOverride All
        Require all granted
    </Directory>

    ErrorLog \${APACHE_LOG_DIR}/web_error.log
    CustomLog \${APACHE_LOG_DIR}/web_access.log combined
</VirtualHost>
EOF

# === 既存の設定を無効化し、新しい設定を有効化 ===
echo "設定を有効化します..."
sudo a2dissite 000-default.conf
sudo a2ensite web.conf
sudo systemctl reload apache2

# === パーミッション確認 ===
echo "Web ディレクトリに実行権限を付与します..."
chmod -R +x "$WEB_DIR"

# === Apache 再起動 ===
echo "Apache を再起動します..."
sudo systemctl restart apache2

echo "✅ セットアップ完了！ http://[サーバーのIPアドレス] にアクセスしてください"
