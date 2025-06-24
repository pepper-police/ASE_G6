from ultralytics import YOLO

# Load a pretrained YOLO11n model
model = YOLO("best_models/0624.pt")

# Define path to the image dir
source = "images"

# Run inference on the source
results = model(source)  # list of Results objects

for i, result in enumerate(results):
    result.save(filename=f"images/prediction_result_{i}.jpg")
    print(f"結果が prediction_result_{i}.jpg に保存されました。")

print("すべての予測結果が画像として保存されました。")
