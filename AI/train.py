from ultralytics import YOLO

# pretrained model (yolo11m.pt)
model = YOLO("yolo11m.pt")
dataset = "datasets/shoes_data.yaml"

results = model.train(data = dataset, epochs=50, imgsz=640)
