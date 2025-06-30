## source ディレクトリの latest.jpg について処理
## 処理済みのデータは archive ディレクトリへ移動
from ultralytics import YOLO
import os
import time
import datetime

model_path = './best_models/0626.pt'
src_dir = './source'
arc_dir = './archive'
latest_file_path = os.path.join(src_dir, 'latest.jpg')

# create dirs
os.makedirs(src_dir, exist_ok=True)
os.makedirs(arc_dir, exist_ok=True)

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
        if os.path.isfile(latest_file_path):
            results = model.track(source=latest_file_path, persist=True,)
            # transform
            res = set()
            if results[0].boxes.id is not None:
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

            # archive
            archive_file_path = os.path.join(arc_dir, datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.jpg')
            results[0].save(filename=f"an{archive_file_path}")
            os.rename(latest_file_path, archive_file_path)

            # print(tracked_objects)
        else:
            print('.', end='', flush=True)
            time.sleep(2)
except KeyboardInterrupt:
    print('\nKeyboard Interrupt')