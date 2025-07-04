## Web
・ルートディレクトリは, /home/ubuntu/webにあるindex.html

・サーバから受け取るデータは, 研究室名（lab_name）, 各来場者のID（user_id）, 入退出の情報（action）, そして入退室した時間（timestamp）を研究室ごとに取得

・サーバ送信されたデータは, /home/ubuntu/web/cgi-bin にある"script.py"でjson型に変換

・変換されたデータを /home/ubuntu/web/data に保存

・/home/ubuntu/web/data に保存されたデータをindex.htmlに反映

ツリー構造
/home/ubuntu/web/
├── cgi-bin
│    └── script.py                      # ここでjson型に変換
├── data 
│    ├── visitor_logs.json              # 各訪問者ごとのIN/OUT
│    ├── current_total_visitor.json     # 各研究室ごとの現在の入場者数      
│    └── current_in.json                # 今現在どの研究室に誰がいるか（INしてOUTしていない人のリスト）
└── index.html