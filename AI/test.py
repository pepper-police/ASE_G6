from ultralytics import YOLO
import time

model = YOLO("./best_models/0722.pt") ## custom model
## src_dir に動画か連続した画像を配置しておく
src_dir = "./source"
res_dir = "./result"

results = model.track(source=src_dir, persist=False, conf=0.5, tracker='./custom_tracker_1.yaml')

for i, frame_result in enumerate(results):
    frame_result.save(filename=f"{res_dir}/result_{i}.jpg")
