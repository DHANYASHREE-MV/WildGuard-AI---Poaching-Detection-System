from ultralytics import YOLO
import numpy as np
import cv2
from PIL import Image

model = YOLO('best.pt')  # Ensure best.pt is in the same directory

def iou(box1, box2):
    """Compute IoU between two boxes (x1, y1, x2, y2)"""
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])
    inter_area = max(0, x2 - x1) * max(0, y2 - y1)

    box1_area = (box1[2] - box1[0]) * (box1[3] - box1[1])
    box2_area = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = box1_area + box2_area - inter_area

    return inter_area / union_area if union_area else 0

def non_max_suppression(boxes, labels, scores, iou_threshold=0.4):
    """Applies NMS and returns filtered boxes"""
    indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    keep = []

    while indices:
        current = indices.pop(0)
        keep.append(current)
        indices = [i for i in indices if labels[i] != labels[current] or iou(boxes[current], boxes[i]) < iou_threshold]

    return keep

def detect_objects(image: Image.Image):
    np_img = np.array(image.convert("RGB"))
    results = model.predict(source=np_img, conf=0.25, save=False, verbose=False)

    poacher_found = False
    result_img = np_img.copy()

    color_map = {
        "poacher": (0, 0, 255),
        "ranger": (0, 255, 0),
        "tourist": (255, 0, 0)
    }

    all_boxes = []
    all_labels = []
    all_scores = []

    for r in results:
        boxes = r.boxes
        if boxes is None or len(boxes) == 0:
            continue

        for box in boxes:
            conf = float(box.conf[0])
            if conf < 0.5:
                continue

            cls_id = int(box.cls[0].item())
            label = model.names[cls_id].strip().lower()
            xyxy = box.xyxy[0].cpu().numpy().astype(int)
            all_boxes.append(xyxy)
            all_labels.append(label)
            all_scores.append(conf)

    # Apply NMS manually
    keep_indices = non_max_suppression(all_boxes, all_labels, all_scores, iou_threshold=0.4)

    for i in keep_indices:
        label = all_labels[i]
        conf = all_scores[i]
        xyxy = all_boxes[i]
        color = color_map.get(label, (255, 255, 255))

        if label == "poacher":
            poacher_found = True

        cv2.rectangle(result_img, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), color, 2)
        text = f"{label.upper()} {conf:.2f}"
        (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(result_img, (xyxy[0], xyxy[1] - th - 5), (xyxy[0] + tw, xyxy[1]), color, -1)
        cv2.putText(result_img, text, (xyxy[0], xyxy[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

    return result_img, poacher_found