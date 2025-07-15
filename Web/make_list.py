# /data フォルダ内のJSONファイル名一覧をJSON形式で返すCGIスクリプト
import os
import json
import traceback

print("Content-Type: application/json\n")

try:
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data"))
    files = [f for f in os.listdir(BASE_DIR) if f.endswith(".json")]
    print(json.dumps(files, ensure_ascii=False, indent=2))
except Exception:
    print(json.dumps({"error": traceback.format_exc()}))
