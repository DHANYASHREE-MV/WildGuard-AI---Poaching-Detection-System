from ultralytics import YOLO

model = YOLO("yolov11_custom.pt")

model.predict(source = "1.jpg", show=True)