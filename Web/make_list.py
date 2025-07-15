# /data フォルダ内のJSONファイル名一覧をJSON形式で返すCGIスクリプト
import os
import json
import traceback

# HTTPレスポンスのヘッダーを出力（Content-TypeはJSON）
print("Content-Type: application/json\n")

try:
    # このスクリプトが置かれているディレクトリの絶対パスを取得
    BASE_DIR = os.path.join(os.path.dirname(__file__))
    # BASE_DIR 内のファイル一覧を取得し、拡張子が .json のものだけを抽出
    files = [f for f in os.listdir(BASE_DIR) if f.endswith(".json")]
    # JSON形式の文字列に変換して出力（日本語も文字化けしないように）
    print(json.dumps(files, ensure_ascii=False, indent=2))
except Exception:
    # エラーが発生した場合、エラーメッセージをJSON形式で出力
    print(json.dumps({"error": traceback.format_exc()}))
