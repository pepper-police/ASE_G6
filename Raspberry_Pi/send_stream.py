import time
import cv2
import imagezmq

serv = 'xxx.xxx.xxx.xxx' # server ip
lab_name = 'xxxx_lab' 

sender = imagezmq.ImageSender(connect_to=f'tcp://{serv}:5555')
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

try:
    while (cap.isOpened()):
        for _ in range(10): #古いバッファを捨てる
            cap.grab()
        ret, frame = cap.read()
        if ret == True:
            reply = sender.send_image(lab_name, frame)
            print(reply.decode())
            time.sleep(10)
except KeyboardInterrupt:
    print('\nKeyboard Interrupt')
