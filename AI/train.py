from ultralytics import YOLO

# pretrained model (yolo11m.pt)
model = YOLO("yolo11m.pt")
dataset = "./shoes_data.yaml"

results = model.train(data = dataset, epochs=100, imgsz=640, project="./runs")
