


```markdown
# 🛡️ Wild Guard AI – Poaching Detection System

**Wild Guard AI** is a real-time object detection system designed to combat wildlife poaching. Built using a custom-trained **YOLOv11 model**, it identifies poachers, rangers, and tourists from uploaded forest surveillance images. If a poacher is detected, the system sends **SMS and voice call alerts** to authorities instantly using **Twilio**, enabling faster response and better protection of wildlife.

---

## 📌 Features

- 🖼️ Multi-image upload support with Streamlit UI
- 🎯 Custom YOLOv11 model for detecting:
  - Poachers
  - Rangers
  - Tourists
- 🧠 Post-processing with Non-Maximum Suppression (NMS) for cleaner results
- 🔔 Instant **SMS & voice call alerts** using Twilio
- 📱 Color-coded bounding boxes and confidence scores
- 💡 Lightweight, fast, and easy to deploy locally

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| [YOLOv11](https://github.com/ultralytics/ultralytics) | Object detection model |
| Streamlit | Web interface for users |
| Twilio API | SMS & voice call alert system |
| OpenCV & Pillow | Image processing |
| Python | Core logic and backend |

---

## 📁 Project Structure

```

wild-guard-ai/
├── app.py                 # Streamlit frontend
├── backend.py             # YOLOv11 detection + NMS logic
├── best.pt                # Trained YOLOv11 model weights
├── .gitignore             # Prevents secrets and large files from being committed
├── .streamlit/
│   └── secrets.toml       # Twilio credentials (excluded from Git)

````

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/wild-guard-ai.git
cd wild-guard-ai
````

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit ultralytics opencv-python pillow twilio
```

### 3. Add your Twilio credentials

Create a file: `.streamlit/secrets.toml`

```toml
[twilio]
account_sid = "your_twilio_account_sid"
auth_token = "your_twilio_auth_token"
from_number = "+1xxxxxxxxxx"
to_number = "+91xxxxxxxxxx"
```

> ⚠️ **Do NOT commit this file to GitHub. It contains secrets.**

### 4. Run the app

```bash
streamlit run app.py
```

---

## 📸 Example Output

* Images with bounding boxes labeled `POACHER`, `RANGER`, or `TOURIST`
* SMS + Call alert when poacher is found
* Real-time image display and results on screen

---

## 🎥 Model Training Reference

This project follows the [YouTube tutorial](https://youtu.be/A1V8yYlGEkI) **“YOLOv11 Object Detection on Custom Dataset | Step‑by‑Step Guide”**, which outlines the process of training YOLOv11 on a custom dataset:

* 🔹 Dataset annotated in YOLO format and split into `train/` and `val/`
* 🔹 Configured using a `data.yaml` file with class names and paths
* 🔹 Training run using:

  ```bash
  yolo detect train data=data.yaml model=yolo11s.pt epochs=50 imgsz=640
  ```
* 🔹 Inference performed using:

  ```python
  model = YOLO('best.pt')
  results = model.predict(source='image.jpg')
  ```

The tutorial helped structure this project's training pipeline and model integration for deployment.

---

## 🔐 Security Notes

* GitHub blocks secret pushes — make sure `.streamlit/secrets.toml` is in `.gitignore`.
* Regenerate your Twilio Auth Token if it was ever accidentally committed.

---

## 🤝 Contributing

Feel free to fork, improve detection logic, or extend to video feeds or live camera streams. PRs welcome!

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

* Ultralytics for YOLOv11
* Twilio for real-time alerts
* [YouTube Tutorial](https://youtu.be/A1V8yYlGEkI) for training guidance
* Wildlife protection efforts that inspired this work

---

```

---



