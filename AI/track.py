## source ディレクトリの latest.jpg について処理
## 処理済みのデータは archive ディレクトリへ移動
from ultralytics import YOLO
import imagezmq
import os
import time
import datetime

model_path = './best_models/0626.pt'
tracker_yaml = './custom_tracker.yaml'

# create hub
image_hub = imagezmq.ImageHub()

print('Loading model...')
model = YOLO(model_path)
print(f'Loaded {model_path}')

## main step
tracked_objects = {}
disappear_timeout = datetime.timedelta(minutes=1)
#disappear_timeout = datetime.timedelta(seconds=10) ## debug

print('Start Tracking... (C-c to exit)')
try:
    while True:
        # receive frame
        rpi_name, frame = image_hub.recv_image()
        print('receive image')
        # YOLO
        results = model.track(source=frame, persist=True)
        res = set()
        if results[0].boxes.id is not None:
            results[0].save(filename=f"latest.jpg")
            res = set(results[0].boxes.id.int().cpu().tolist())

        current_time = datetime.datetime.now()
        # update detected objects
        for obj_id in res:
            # objects detected for the first time
            if obj_id not in tracked_objects:
                tracked_objects[obj_id] = {
                    'first' : current_time,
                    'last' : current_time
                }
            else:
                tracked_objects[obj_id]['last'] = current_time
        
        # check objects
        del_list = []
        for obj_id, data in tracked_objects.items():
            # objects no longer detected
            if obj_id not in res:
                # a minute elapsed without detection
                time_delta = current_time - data['last']
                if time_delta > disappear_timeout:
                    # print duration
                    duration = (data['last'] - data['first']).total_seconds()
                    print(f"id:{obj_id} -- {duration}s")
                    del_list.append(obj_id)
        for obj_id in del_list:
            del tracked_objects[obj_id]

        image_hub.send_reply(b'OK')
        print('send OK')
except KeyboardInterrupt:
    print('\nKeyboard Interrupt')