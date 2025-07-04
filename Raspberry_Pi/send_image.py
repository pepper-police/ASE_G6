import cv2
import requests
import time

def capture_image(filename='capture.jpg'):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("カメラが開けません")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filename, frame)
    else:
        raise IOError("画像キャプチャに失敗")

    cap.release()

def send_image_to_server(filename, server_url):
    with open(filename, 'rb') as f:
        files = {'image': f}
        response = requests.post(server_url, files=files)
        print(f"[{response.status_code}] {response.text}")

if __name__ == '__main__':
    server_url = 'http://34.231.228.246:5000/upload'  # EC2のIPに変更

    while True:
        try:
            capture_image()
            send_image_to_server('capture.jpg', server_url)
        except Exception as e:
            print(f"エラー: {e}")

        time.sleep(5)  # 5秒待機