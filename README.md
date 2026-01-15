# VisualAssist Classroom 🎓

An inclusive learning tool designed for students with visual impairments. 
This project uses **Python (Flask)** and **Google Cloud Vision AI** to provide 
real-time audio descriptions of classroom boards, diagrams, and physical obstacles.

## 🚀 Features
- **OCR Reading**: Digitizes handwritten board notes.
- **Diagram Analysis**: Explains complex charts and graphs.
- **Navigation Assistance**: Identifies obstacles and people in the surroundings.
- **Accessibility First**: High-contrast UI and built-in Text-to-Speech.

## 🛠️ Tech Stack
- **Frontend**: HTML5, CSS3 (Modern UI), JavaScript (Web Speech API).
- **Backend**: Python 3, Flask, Google Cloud Vision SDK.
- **Environment**: Zorin OS / Linux.

## ⚙️ Setup
1. Place your Google Cloud `service-account.json` in the `/backend` folder.
2. Install dependencies: `pip install -r backend/requirements.txt`.
3. Run the backend: `python backend/app.py`.
4. Open `frontend/index.html` in your browser.
