WireGuardをインストールする
-----------------------------------
$ sudo apt -y install wireguard-tools iptables
-----------------------------------
WireGuardの設定を行う
-----------------------------------
root@dlp:~# umask 077
# サーバー用プライベートキー作成
root@dlp:~# wg genkey | tee /etc/wireguard/server.key
gCS9F2qcHIPyacpLC4z7wA1bXuaz99ts1RCDxP1ym3Y=
# サーバー用パブリックキー作成
root@dlp:~# cat /etc/wireguard/server.key | wg pubkey | tee /etc/wireguard/server.pub
ZLyTvWsPlly4vmqqLwXcQ194E1xgBWGHb0+n98RiSiM=
# クライアント用プライベートキー作成
root@dlp:~# wg genkey | tee /etc/wireguard/client.key
MDuvBHtO9FI1jetfTCHaB1rmOTJRtPI9Xnu+FTk29m0=
# クライアント用パブリックキー作成
root@dlp:~# cat /etc/wireguard/client.key | wg pubkey | tee /etc/wireguard/client.pub
K03BktxiXod16UCF7zx8KfXu5Uhfd4ItGefrB9TkUAg=
# ネットワーク インターフェース 確認
root@dlp:~# ip addr
-----------------------------------

設定ファイルを新規で作成する
-----------------------------------
root@dlp:~# vi /etc/wireguard/wg0.conf
[Interface]
PrivateKey = サーバ用秘密鍵
Address = 10.0.0.1
ListenPort = 51820

[Peer]
PublicKey = クライアント用公開鍵
AllowedIPs = 10.0.0.0/24
-----------------------------------
VPNサーバーの起動
-----------------------------------
root@dlp:~# systemctl start wg-quick@wg0
root@dlp:~# ip addr
    ...
    3: wg0: <POINTOPOINT,NOARP,UP,LOWER_UP> mtu 1420 qdisc noqueue state UNKNOWN group default qlen 1000
    link/none
    inet 172.16.100.1/32 scope global wg0
       valid_lft forever preferred_lft forever

    
以上でサーバー側の設定が終了