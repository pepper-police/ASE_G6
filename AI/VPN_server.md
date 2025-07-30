# サーバ側 VPN セットアップ手順

### WireGuard のインストール
```bash
apt install wireguard-tools iptables
```

### 接続用鍵の作成
サーバ用秘密鍵・公開鍵の作成
```
umask 077
wg genkey > /etc/wireguard/server.key
wg genkey < /etc/wireguard/server.key > server.pub
```
クライアント用秘密鍵・公開鍵の作成
```
wg genkey > /etc/wireguard/client.key
wg genkey < /etc/wireguard/client.key > client.pub
```

### 設定ファイルの作成
```config
[Interface]
PrivateKey = サーバ用秘密鍵
Address = 10.0.0.1
ListenPort = 51820

[Peer]
PublicKey = クライアント用公開鍵
AllowedIPs = 10.0.0.0/24
```
上記の様なファイルを `/etc/wireguard/wg0.conf` に作成

### VPN 有効化
```bash
systemctl start wg-quick@wg0
```
