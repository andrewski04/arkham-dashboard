# Arkham Security Dashboard Prototype

This is a prototype for the **Project Arkham** security dashboard. It's a simple web app with a frontend dashboard and a backend API that serves dummy data for testing. The goal is to simulate what a real security monitoring system might look like.

---

## Overview

- **Backend:** A Flask server with multiple API endpoints that return fake security data (network logs, server logs, video feeds, biometric access, physical security events, internal communications, inmate threats, and more).
- **Frontend:** A dashboard built with HTML, CSS, and JavaScript. It fetches data from the backend APIs and displays it in different views.
- **Dummy Data:** The APIs don't connect to real systems, they just generate sample data to be displayed on the dashboard.

---

## Set up environment

1. **Clone this repository**

   Download or clone the repo to your computer.

2. **Create a virtual environment (recommended)**

   Open a terminal in the project folder and run:

   ```
   python -m venv .venv
   ```

3. **Activate the virtual environment**


    ```
    .\.venv\Scripts\activate
    ```

4. **Install the dependencies**

   ```
   pip install -r requirements.txt
   ```

5. **Run the app**

   - If using the virtual environment:

     ```
     python run.py
     ```

   - Or, if not using a virtual environment:

     ```
     py run.py
     ```

6. **Open the dashboard**

   Go to [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser. You should see the main dashboard page.

---

## Project structure

```
arkham-dashboard/
│
├── run.py                  # Entry point to start the Flask server
├── requirements.txt        # Python dependencies
├── README.MD               # This file
│
├── app/
    ├── __init__.py         # Creates the Flask app and registers blueprints
    ├── routes.py           # Frontend routes (renders HTML pages)
    │
    ├── api/                # API endpoints serving dummy data
    │   ├── network.py
    │   ├── server_logs.py
    │   ├── video_surveillance.py
    │   ├── ...
    │
    ├── templates/          # HTML templates
    │   ├── base.html               # Base layout
    │   ├── dashboard.html          # Main dashboard
    │   ├── network.html
    │   ├── server_logs.html
    │   ├── video_surveillance.html
    │   ├── ...  # Other endpoints specific logs
    │
    └── static/ # Static files like CSS, JS, images
        ├── css/
        │   └── style.css
        └── js/
            ├── core.js
            ├── dashboard.js
            ├── dashboard-view.js
            ├── log-view.js
            └── utils.js

```




