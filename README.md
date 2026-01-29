# Conserving-Wildlife-through-Poaching-Detection
An AI powered real-time surveillance system that detects and identifies poachers from video footage using YOLOv8, RetinaFace, and DeepFace, supporting wildlife conservation through automated monitoring, alerts, and reporting.

# Wildlife Conservation: Poaching Detection Using YOLOv8

Illegal poaching is one of the most critical threats to global biodiversity. This project presents an **AI-based intelligent surveillance system** that automatically detects and identifies poachers from video footage using advanced **deep learning and computer vision techniques**. The system is designed to assist wildlife authorities by enabling real-time monitoring, automated alerts, and evidence-based reporting.



## Objective of the System

The primary objective of this project is to design and implement a **real-time poaching detection and identification system** that supports wildlife conservation efforts by enabling immediate response to illegal activities.

### Specific Objectives:
1. **Automated Video Analysis**  
   Analyze surveillance footage to detect unauthorized human presence in protected wildlife areas.

2. **Real-Time Poacher Detection**  
   Use the **YOLOv8 object detection model** to accurately and efficiently detect poachers from video frames.

3. **Facial Detection and Recognition**  
   Integrate **RetinaFace** for face detection and **DeepFace** for facial recognition to identify individuals involved in poaching.

4. **Redundancy Elimination**  
   Apply **cosine similarity on facial embeddings** to filter duplicate detections and count only unique poacher identities.

5. **User Interface for Monitoring**  
   Provide a **Streamlit-based web application** for uploading videos, visualizing detections, and downloading reports.

6. **Alert Mechanisms**  
   Automatically send **email alerts** to forest or enforcement authorities with timestamped evidence.

7. **Alarm / Siren Activation**  
   Trigger an audible alarm at the surveillance location to deter poachers and alert nearby personnel.

8. **Operational Efficiency**  
   Reduce reliance on manual monitoring and improve surveillance coverage through intelligent automation.

9. **System Extensibility**  
   Enable future integration with drones, GPS-based mapping, mobile notifications, and thermal imaging systems.


## Proposed Solution

Traditional wildlife monitoring relies heavily on manual patrols and post-event video analysis, which is time-consuming and error-prone. This project proposes an **AI-driven automated surveillance solution** that enhances efficiency and response time.

### Key Benefits:
- **Reduced Manual Monitoring**  
  Automates hours of video analysis, minimizing human workload.

- **Real-Time Intervention**  
  Enables instant detection and alerting, reducing the likelihood of successful poaching.

- **Evidence-Based Reporting**  
  Generates timestamped visual evidence and structured reports for legal and investigative use.

- **Poacher Identification & Tracking**  
  Facial recognition helps identify repeat offenders across multiple incidents.

- **Decision Support for Authorities**  
  Empowers forest officials with an intelligent, reliable monitoring tool.



## Developer & Research Contributions

As the **developer and researcher** for this project, I was responsible for the complete end-to-end implementation and research.

### Key Contributions:
- **Literature Review**  
  Conducted extensive research on wildlife monitoring systems, object detection models (YOLOv8), and facial recognition frameworks (RetinaFace, DeepFace) to establish a strong theoretical foundation.

- **Dataset Collection**  
  Curated datasets from open-source platforms such as **Kaggle**, focusing on human detection in outdoor environments due to the lack of direct poaching datasets.

- **Data Preprocessing**  
  Processed videos and images using **OpenCV**, including frame extraction, resizing, cleaning, annotation, and dataset organization for YOLOv8 training.

- **Model Training & Integration**  
  Trained a custom **YOLOv8** object detection model and integrated **RetinaFace** for face localization and **DeepFace** for identity embedding generation.

- **Web Interface Development**  
  Built a **Streamlit-based application** to visualize detections, upload video footage, and generate downloadable poacher identification reports.


## Technology Stack

| Module | Technology |
|------|-----------|
| Object Detection | YOLOv8 |
| Video Processing | OpenCV |
| Facial Detection | RetinaFace |
| Facial Recognition | DeepFace |
| Web Application | Streamlit |
| Email Alerts | smtplib, Gmail SMTP |
| Environment Handling | Python-dotenv |
| Dataset Annotation | Roboflow / LabelImg |
| Programming Language | Python |



## Project Structure

wildlife-poaching-detection/
│
├── data/ # Images, videos, datasets
├── models/ # Trained YOLOv8 models
├── notebooks/ # Experiments & analysis
├── src/
│ ├── preprocessing.py
│ ├── train.py
│ ├── detect.py
│ ├── face_recognition.py
│ └── alert_system.py
│
├── reports/ # Generated detection reports
├── app.py # Streamlit web app
├── requirements.txt
└── README.md

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/wildlife-poaching-detection.git
Install dependencies:
pip install -r requirements.txt


Run the Streamlit app:
streamlit run app.py

Future Enhancements:


Drone-based real-time video integration.
GPS-based poacher tracking and heatmaps.
Mobile alert notifications.
Thermal imaging support for night surveillance.

License:
This project is licensed under the MIT License.

Impact:
This system demonstrates how AI-driven surveillance can play a critical role in wildlife protection by improving response times, reducing illegal activity, and supporting global conservation initiatives.






