# run this program on each RPi to send a labelled image stream
# you can run it on multiple RPi's; 8 RPi's running in above example

import cv2
import imagezmq

serv = ''
sender = imagezmq.ImageSender(connect_to='tcp://{serv}:5555')
cap = cv2.VideoCapture(0)

while (cap.isOpened()):
    # 古いフレームを捨てて最新に近いものを取得
    for _ in range(5):  # バッファにある古いフレームを5枚捨てる
        cap.grab()
    ret, frame = cap.read()
    if ret == True:
        sender.send_image('test', frame)