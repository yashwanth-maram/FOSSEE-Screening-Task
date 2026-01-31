# 🧪 Chemical Equipment Parameter Visualizer

> **Hybrid Web + Desktop Application** for CSV-based chemical equipment analytics with interactive visualizations.

[![Backend](https://img.shields.io/badge/Backend-Django%20REST-092E20?style=for-the-badge&logo=django)](https://chemical-equipment-backend-g7ls.onrender.com)
[![Frontend](https://img.shields.io/badge/Frontend-React%20+%20Vite-61DAFB?style=for-the-badge&logo=react)](https://chemical-equipment-frontend.vercel.app)
[![Desktop](https://img.shields.io/badge/Desktop-PyQt5-41CD52?style=for-the-badge&logo=python)](./desktop_app)

---

## 🚀 Live Demo

| Platform | URL |
|----------|-----|
| 🌐 **Web Application** | **[chemical-equipment-frontend.vercel.app](https://chemical-equipment-frontend.vercel.app)** |
| ⚙️ **Backend API** | **[chemical-equipment-backend-g7ls.onrender.com](https://chemical-equipment-backend-g7ls.onrender.com)** |

### Demo Credentials
```
Username: demo
Password: demo1234
```

---

## 📋 Features

- ✅ **CSV Upload & Analysis** — Upload equipment data and get instant statistical insights
- ✅ **Interactive Charts** — Bar charts via Chart.js (Web) and Matplotlib (Desktop)
- ✅ **Dataset History** — View last 5 uploaded datasets with timestamps
- ✅ **PDF Reports** — Download comprehensive reports with embedded charts
- ✅ **Dual Platform** — Consistent experience across Web and Desktop

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend API | Django + Django REST Framework |
| Web Frontend | React.js (Vite) + Chart.js |
| Desktop Frontend | PyQt5 + Matplotlib |
| Database | SQLite |
| Data Processing | Pandas |
| Version Control | Git & GitHub |

---

## Project Structure

```
chemical-equipment-visualizer/
│
├── backend/
│   ├── config/                 # Django project settings
│   │   ├── settings.py
│   │   └── urls.py
│   ├── equipment/              # Main Django app
│   │   ├── models.py           # Dataset model
│   │   ├── views.py            # API views
│   │   ├── serializers.py      # DRF serializers
│   │   └── urls.py             # API routes
│   ├── requirements.txt
│   └── manage.py
│
├── web-frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Login.jsx       # Authentication page
│   │   │   └── Upload.jsx      # Main dashboard
│   │   ├── components/
│   │   │   ├── Charts.jsx      # Chart.js visualizations
│   │   │   └── History.jsx     # Dataset history list
│   │   ├── api.js              # Axios configuration
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
├── desktop_app/
│   ├── main.py                 # Application entry point
│   ├── api_client.py           # HTTP client with session handling
│   ├── login_window.py         # Login UI
│   ├── upload_window.py        # Main window
│   ├── history_widget.py       # History display
│   ├── charts_widget.py        # Matplotlib charts
│   └── requirements.txt
│
├── sample_equipment.csv        # Sample CSV for testing
└── README.md
```

---

## Installation and Setup

### Prerequisites

- Python 3.10+
- Node.js 18+
- pip and npm

---

### 1️⃣ Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create demo user (first time only)
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_user('demo', 'demo@example.com', 'demo1234') if not User.objects.filter(username='demo').exists() else print('User exists')"

# Start the server
python manage.py runserver
```

> 🟢 Backend runs at: `http://127.0.0.1:8000`

---

### 2️⃣ Web Frontend Setup

```bash
# Navigate to web frontend directory
cd web-frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

> 🟢 Web app runs at: `http://localhost:5173`

---

### 3️⃣ Desktop Application Setup

```bash
# Navigate to desktop app directory
cd desktop_app

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

A native desktop window will open.

---

## 🔗 API Reference

All endpoints are prefixed with `/api/`

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/csrf/` | GET | Public | Get CSRF cookie |
| `/login/` | POST | Public | Authenticate user |
| `/upload-csv/` | POST | Public | Upload CSV & get analytics |
| `/history/` | GET | Public | Get last 5 datasets |
| `/pdf/` | GET | Public | Download PDF report |

---

## 📊 CSV Format

The application expects CSV files with these columns:

| Column | Type | Example |
|--------|------|---------|
| Equipment Name | String | Pump-001 |
| Type | String | Pump, Valve, Compressor |
| Flowrate | Numeric | 150.5 |
| Pressure | Numeric | 45.2 |
| Temperature | Numeric | 85.0 |

### Sample CSV

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,150.5,45.2,85.0
Valve-002,Valve,200.0,30.5,72.0
Compressor-003,Compressor,180.0,60.0,95.5
```

> 📁 Use `sample_equipment.csv` included in the repository for testing.

---

## ✅ Quick Test

1. Start backend server (`python manage.py runserver`)
2. Start web frontend (`npm run dev`) or launch desktop app (`python main.py`)
3. Login with demo credentials
4. Upload `sample_equipment.csv`
5. View analytics and charts
6. Check history and download PDF report

---

## 📝 License

Developed as part of the **FOSSEE Semester Long Internship** screening task.

---

<p align="center">
  <strong>Built with ❤️ using Django, React, and PyQt5</strong>
</p>
