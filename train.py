from ultralytics import YOLO

model = YOLO("yolo11m.pt")

model.train(data = "dataset_custom.yaml",imgsz = 640, batch = 8 , epochs = 100, workers = 100,device = 0 )