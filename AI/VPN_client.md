WireGuard をインストール

-----------------------------------
root@client:~# apt -y install wireguard-tools
-----------------------------------
WireGuardの設定
-----------------------------------
root@client:~# umask 077
# 設定ファイル新規作成
root@client:~# vi /etc/wireguard/wg0.conf
[Interface]
PrivateKey = クライアント用秘密鍵
Address = 10.0.0.2

[Peer]
PublicKey = サーバ用公開鍵
AllowedIPs = 10.0.0.1

EndPoint = サーバIP:51820
-----------------------------------
VPNの起動と接続状態の確認
-----------------------------------
root@client:~# wg-quick up wg0
root@client:~# ip addr
root@client:~# wg show
-----------------------------------
最後にPingが通れば完成
-----------------------------------
root@client:~# ping -c 3 10.0.0.1
-----------------------------------
