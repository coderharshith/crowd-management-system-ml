# 🚨 Crowd Management System

A Python-based **AI-powered Crowd Management and Monitoring System** that uses computer vision, YOLO object detection, tracking, social-distancing analysis, activity detection, and crowd monitoring to improve crowd safety and management.

## 🎥 Demo Video

<video src="./demo.mp4" controls width="100%"></video>

**Demo:** `demo.mp4`
---

## 📌 About the Project

The **Crowd Management System** is designed to monitor and analyze crowd activity from video footage.

The system uses **YOLOv8, OpenCV, Python, and computer vision techniques** to detect and track people, monitor crowd activity, identify specific events, and generate alerts.

It also provides a web-based dashboard for monitoring and managing the system.

---

## ✨ Key Features

### 👥 Crowd Detection
- Detect people in video using YOLOv8
- Count detected people
- Track people across video frames
- Monitor crowd movement

### 🚨 Activity Detection
- Detect unusual crowd activity
- Monitor crowd behavior
- Generate alerts for detected events
- Maintain activity logs

### 📏 Social Distancing
- Monitor distance between detected people
- Identify possible social-distancing violations
- Display monitoring results on the dashboard

### 🚪 Gate Management
- Gate monitoring and control
- Gate event logging
- Monitor entry/exit-related events

### 🗺️ Zone Monitoring
- Define monitoring zones
- Store zone information
- Monitor activity inside configured areas

### 🎥 Video Monitoring
The system supports video-based monitoring.


The video is processed frame-by-frame for:

- Person detection
- Person tracking
- Crowd counting
- Activity detection
- Social-distance analysis
- Zone monitoring
- Alert generation

### 📊 Dashboard

The web dashboard provides a centralized interface for:

- Starting monitoring
- Viewing detection results
- Monitoring crowd activity
- Viewing alerts
- Checking logs
- Managing monitoring operations

### 🔐 User Authentication

The application includes user account functionality.

Users can:

- Create an account
- Login
- Access the monitoring dashboard
- Start crowd monitoring

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application/backend |
| Flask-CORS | Cross-origin communication |
| YOLOv8 | Object/person detection |
| Ultralytics | YOLO implementation |
| OpenCV | Video and image processing |
| PyTorch | Deep learning framework |
| NumPy | Numerical processing |
| SciPy | Scientific calculations |
| FilterPy | Tracking/filtering |
| Matplotlib | Data visualization |
| Firebase Admin | Firebase integration |
| MongoDB / PyMongo | Database support |
| Streamlit | Dashboard/UI support |

The project dependencies are defined in `requirements.txt`.

---

# 💻 Requirements

Before running the project, make sure you have:

- Python 3.9 or newer
- pip
- Git
- Windows/Linux/macOS
- Required Python packages
- Video file for monitoring

### Recommended

For faster YOLO processing:

- NVIDIA GPU
- CUDA-compatible PyTorch installation

---

# 🚀 Installation

## 1. Open the Project Folder

Open a terminal inside the project directory.

Example:

```bash
cd crowd-management
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate the environment:

```bash
.\venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

---

# 📦 Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

The supplied project instructions use the same virtual-environment and dependency-installation process.

---

# ▶️ Run the Application

After activating the virtual environment:

```bash
cd backend
```

Then run:

```bash
python dashboard_app.py
```

The provided project run instructions use `dashboard_app.py` as the main application entry point.

---

# 🌐 Open the Dashboard

After the server starts, open your browser and visit:

```text
http://localhost:5000
```



---

# 🔐 Login

When the dashboard opens:

1. Create a new account.
2. Login using your credentials.
3. Open the monitoring dashboard.
4. Start the monitoring process.

The supplied run instructions follow this login → dashboard → monitoring flow.

---

### Monitoring Flow

```text
Video
  ↓
OpenCV
  ↓
YOLOv8 Detection
  ↓
Person Detection
  ↓
Object Tracking
  ↓
Crowd Analysis
  ↓
Activity Detection
  ↓
Social Distance Analysis
  ↓
Zone / Gate Monitoring
  ↓
Alerts & Logs
  ↓
Dashboard
```

---

# 🤖 YOLOv8 Model

The project contains a YOLO model used for object detection.

```text
yolov8s.pt
```

The model is used as part of the computer-vision detection pipeline.

---

# 📊 Crowd Monitoring

The monitoring system can provide information such as:

- Number of detected people
- Crowd activity
- Person tracking
- Social-distance violations
- Zone activity
- Gate events
- Alerts
- Monitoring logs

---

# 🚨 Alerts & Logs

The system maintains monitoring information through log files such as:

```text
alerts_log.txt
gate_events.log
```

These logs can be used to review detected alerts and gate-related events.

---

# ⚙️ Configuration

The backend contains configuration files such as:

```text
config.json
zone_data.json
```

These files can be used to configure application and zone-related settings.

**Do not modify configuration values unless you understand how they are used by the application.**

---

# 🗄️ Database

The project includes a local database:

```text
users.db
```

This database is used by the application for user-related data.

---

# 📁 Important Files

### Backend

```text
activity_detector.py
```

Handles activity detection functionality.

```text
dashboard_app.py
```

Main dashboard/application entry point.

```text
firebase_config.py
```

Firebase-related configuration.

```text
gate_controller.py
```

Handles gate-control functionality.

```text
social_distancing.py
```

Handles social-distance monitoring.

```text
yolov8s.pt
```

YOLOv8 model used for detection.

```text
config.json
```

Application configuration.

```text
zone_data.json
```

Zone configuration/data.

```text
alerts_log.txt
```

Alert log.

```text
gate_events.log
```

Gate event log.

---

# 🧪 Basic Testing

After starting the application:

1. Open `http://localhost:5000`
2. Create an account.
3. Login.
4. Open the dashboard.
5. Start monitoring.
6. Select/use the crowd video.
7. Check person detection.
8. Check crowd monitoring.
9. Check alerts and logs.

---

# 🐛 Troubleshooting

## Python is not recognized

Check Python:

```bash
python --version
```

If Python is installed but not recognized, add Python to your system PATH.

---

## Virtual Environment Not Activated

Windows:

```bash
.\venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

---

## Missing Dependencies

Run:

```bash
pip install -r requirements.txt
```

---

## Application Not Opening

Make sure you are running the application from the backend directory:

```bash
cd backend
python dashboard_app.py
```

Then open:

```text
http://localhost:5000
```

---

## Video Not Processing

Check:

- The video file exists.
- The video format is supported.
- The video is not corrupted.
- YOLO model is available.
- Required Python packages are installed.
- The application has access to the video file.

---

# 🔒 Security Recommendations

Before deploying this project publicly:

- Do not expose database credentials.
- Do not commit Firebase private credentials.
- Do not commit `.env` files.
- Validate uploaded videos.
- Restrict uploaded file sizes.
- Protect user authentication.
- Use HTTPS in production.
- Restrict access to monitoring data.

---

# 🚀 Future Improvements

Possible improvements include:

- 📹 Multiple CCTV camera support
- 🔴 Real-time camera streaming
- 📱 Mobile monitoring application
- 🗺️ Live crowd heatmaps
- 🚨 Automatic emergency alerts
- 📧 Email notifications
- 📲 SMS notifications
- 📊 Advanced crowd analytics
- 🤖 Abnormal behavior detection
- ☁️ Cloud deployment
- 📈 Historical crowd reports
- 🎥 Automatic incident recording

---

# ▶️ Quick Start

Run the following commands:

```bash
python -m venv venv
```

```bash
.\venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

```bash
cd backend
```

```bash
python dashboard_app.py
```

Then open:

```text
http://localhost:5000
```

Create an account, login, and start monitoring.

---

# 📜 License

Add your preferred license here.

Example:

```text
MIT License
```

---

## 👨‍💻 Crowd Management System

**AI-powered crowd monitoring using Python, YOLOv8, OpenCV, and computer vision.**
