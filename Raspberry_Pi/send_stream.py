import time
import cv2
import imagezmq

serv = '172.21.50.100' ## server ip

sender = imagezmq.ImageSender(connect_to=f'tcp://{serv}:5555')
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

try:
    while (cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            reply = sender.send_image('test', frame)
            print(reply.decode())
            time.sleep(1)
except KeyboardInterrupt:
    print('\nKeyboard Interrupt')
