# クライアント側 VPN セットアップ手順

### WireGuard のインストール
```bash
apt install wireguard
```

### 設定ファイルの作成
```conf
[Interface]
PrivateKey = クライアント用秘密鍵
Address = 10.0.0.2

[Peer]
PublicKey = サーバ用公開鍵
AllowedIPs = 10.0.0.1

EndPoint = サーバIP:51820
```
上記の様なファイルを `/etc/wireguard/wg0.conf` として作成

### VPN 有効化・疎通確認
```bash
wg-quick up wg0
ping -c 10.0.0.1
```
サーバ側・クライアント側双方の設定が問題なければ ping が通る