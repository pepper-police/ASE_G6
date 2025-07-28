# ストリームで送られるデータを処理
from ultralytics import YOLO
import zmq
import imagezmq
import datetime
import json
import os

model_path = './best_models/0722.pt'
tracker_yaml = './custom_tracker.yaml'
json_path = '../Web/'
disappear_timeout = datetime.timedelta(minutes=1)
min_duration = datetime.timedelta(minutes=1)

# create hub
image_hub = imagezmq.ImageHub()

# for each lab
yolo_models = {}
tracking_data = {}

## main step
print('Start Tracking... (C-c to exit)')
try:
    while True:
        # receive frame (polling)
        if image_hub.zmq_socket.poll(1000): # 1000 milliseconds
            lab_name, frame = image_hub.recv_image()
            print(f"receive frame from {lab_name}")
        else:
            continue

        current_time = datetime.datetime.now()

        # get the YOLO model instance and tracking data for the current lab
        if lab_name not in yolo_models:
            print(f"create new instance for lab : {lab_name} ...")
            yolo_models[lab_name] = YOLO(model_path)
            print("Done")
            tracking_data[lab_name] = {}
        model = yolo_models[lab_name]
        tracked_objects = tracking_data[lab_name]

        # tracking
        results = model.track(source=frame, persist=True, verbose=False, conf=0.5)
        results[0].save(filename=f"../Web/debug/{lab_name}_latest.jpg") # debug image

        # create detected objects list
        detected_objects = []
        if results[0].boxes.id is not None:
            cls_name = model.names
            for id, box in enumerate(results[0].boxes):
                detected_objects.append({
                    'id': int(box.id.item()),
                    'class': cls_name[int(box.cls.item())],
                    'box': box.xyxy[0].tolist()
                })
            # create shoes, tag list
            shoes_list = [d for d in detected_objects if d['class'] == 'shoes']
            tag_list = [d for d in detected_objects if d['class'] == 'tag']
            # find tagged shoes
            tagged_shoes = set()
            for tag in tag_list:
                # default value
                min_dist = float('inf')
                closest_id = None
                # tag center
                tag_cx = (tag['box'][0] + tag['box'][2]) / 2
                tag_cy = (tag['box'][1] + tag['box'][3]) / 2
                for shoes in shoes_list:
                    # shoes center
                    shoes_cx = (shoes['box'][0] + shoes['box'][2]) / 2
                    shoes_cy = (shoes['box'][1] + shoes['box'][3]) / 2
                    dist_sq = (tag_cx - shoes_cx)**2 + (tag_cy - shoes_cy)**2
                    if dist_sq < min_dist:
                        min_dist = dist_sq
                        closest_id = shoes['id']
                # mark tagged shoes
                if closest_id is not None:
                    tagged_shoes.add(closest_id)

            # track only untagged shoes
            detected_ids = set()
            for obj in shoes_list:
                obj_id = obj['id']
                if obj_id not in tagged_shoes:
                    detected_ids.add(obj_id)
                    # update the last seen time for detected objects
                    if obj_id not in tracked_objects:
                        tracked_objects[obj_id] = {
                            'first': current_time,
                            'last': current_time
                        }
                    else:
                        tracked_objects[obj_id]['last'] = current_time

        # create json log
        json_log = []
        for obj_id, data in tracked_objects.items():
            # only add over min_duration
            if data['last'] - data['first'] > min_duration:
                end_time = None
                if current_time - data['last'] > disappear_timeout:
                    end_time = data['last'].strftime('%Y-%m-%dT%H:%M:%S')
                entry = {
                    "id": obj_id,
                    "start": data['first'].strftime('%Y-%m-%dT%H:%M:%S'),
                    "end": end_time
                }
                json_log.append(entry)

        # write to temporary JSON file
        output_json = {
            "lab_name": lab_name,
            "data": json_log
        }
        with open(f"{lab_name}.tmp", 'w') as f:
            json.dump(output_json, f, indent=4)
        # rename temporary file
        os.replace(f"{lab_name}.tmp", f"{json_path}{lab_name}.json")
        print(f"create {lab_name}.json")

        image_hub.send_reply(b'OK')
except KeyboardInterrupt:
    print('\nKeyboard Interrupt')
