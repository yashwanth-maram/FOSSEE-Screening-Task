# Chemical Equipment Parameter Visualizer

**Hybrid Web + Desktop Application**

A data visualization system that allows users to upload CSV files containing chemical equipment data, performs statistical analysis via a Django REST API, and presents results through both a React web interface and a PyQt5 desktop application.

This project was developed to satisfy the **FOSSEE Semester Long Internship screening task**, focusing on CSV-based analytics, shared backend APIs, and dual Web + Desktop visualization.

---

## Demo Credentials

To simplify evaluation, a demo account is provided:

```
Username: demo
Password: demo1234
```

---

## Technology Stack

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

### 1. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The backend API runs at: `http://127.0.0.1:8000`

### 2. Web Frontend Setup

```bash
cd web-frontend
npm install
npm run dev
```

The web application runs at: `http://localhost:5173`

### 3. Desktop Application Setup

```bash
cd desktop_app
pip install -r requirements.txt
python main.py
```

A native desktop window will open.

---

## API Reference

All endpoints are prefixed with `/api/`.

| Endpoint | Method | Authentication | Description |
|----------|--------|----------------|-------------|
| `/csrf/` | GET | Public | Returns CSRF cookie |
| `/login/` | POST | Public | Authenticates user and starts session |
| `/auth-status/` | GET | Required | Checks authentication status |
| `/upload-csv/` | POST | Public | Uploads CSV and returns analytics |
| `/history/` | GET | Public | Returns last 5 uploaded datasets |
| `/pdf/` | GET | Public | Generates and returns PDF report |

### Authentication

The application uses Django's session-based authentication. Both frontends:

1. Fetch a CSRF token via `GET /api/csrf/`
2. Submit credentials via `POST /api/login/`
3. Maintain session cookies for subsequent authenticated requests

---

## CSV File Format

The application expects CSV files with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| Equipment Name | String | Equipment identifier |
| Type | String | Category (Pump, Valve, etc.) |
| Flowrate | Numeric | Flow rate value |
| Pressure | Numeric | Pressure value |
| Temperature | Numeric | Temperature value |

### Example

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-001,Pump,150.5,45.2,85.0
Valve-002,Valve,200.0,30.5,72.0
Compressor-003,Compressor,180.0,60.0,95.5
```

A sample file `sample_equipment.csv` is included in the repository.

---

## Features Implemented

### CSV Upload and Analytics

- CSV validation and column checking
- Server-side parsing using Pandas
- Computation of:
  - Total equipment count
  - Average flowrate
  - Average pressure
  - Average temperature
  - Equipment type distribution

### Data Visualization

- **Web**: Bar charts using Chart.js
- **Desktop**: Embedded Matplotlib charts within PyQt5

### History Management

- Maintains a rolling history of the last 5 uploaded datasets (global, as per task specification)
- Displays filename and upload timestamp

### PDF Report Generation

- Generated server-side using ReportLab
- Includes summary statistics and visual charts
- Downloaded via authenticated endpoint

### Authentication

- Session-based authentication using Django
- CSRF protection for all state-changing requests
- Shared authentication flow across Web and Desktop clients

---

## Design Decisions

### Shared Backend

A single Django REST backend serves both the Web and Desktop applications, ensuring consistent analytics and data handling.

### Server-Side Analytics

All CSV parsing and statistical computation occur on the backend. Frontends are purely presentational and consume pre-computed results.

### Session-Based Authentication

Django session authentication was chosen for simplicity and reliability, avoiding token management while supporting both browser and desktop clients.

### Minimal UI

The UI is intentionally minimal to emphasize correctness, clarity, and architectural alignment over visual complexity.

### Admin Panel (Optional)

Django's admin panel is enabled for inspecting stored datasets and verifying backend persistence. It is not required for normal application usage.

---

## Manual Verification Steps

1. Start the backend server
2. Launch the web or desktop client
3. Login using demo credentials
4. Upload `sample_equipment.csv`
5. Verify analytics display and charts render
6. Check history shows the upload
7. Download PDF and verify it contains charts

---

## Dependencies

### Backend (`backend/requirements.txt`)
- Django
- djangorestframework
- django-cors-headers
- pandas
- reportlab
- matplotlib

### Web Frontend (`web-frontend/package.json`)
- react
- axios
- chart.js
- react-chartjs-2

### Desktop (`desktop_app/requirements.txt`)
- PyQt5
- requests
- matplotlib

---

## Author

Developed as part of the **FOSSEE Semester Long Internship** screening task.
