# 🧺 osheet-backend

This is the backend service for the **O'Sheet** mobile app. It manages linen cabinet images for each floor, allowing you to upload and retrieve the latest image per floor. Built with **Flask**, it uses **SQLite** for storage and is ready for deployment using **Gunicorn** and **Docker**.

---

## 🚀 Features

- 📸 Upload base64-encoded images per floor
- 🗂 Retrieve the latest image for a given floor
- 🛢 Lightweight SQLite database
- 🐳 Dockerized for local or production deployment
- 🔥 Gunicorn WSGI server for production use

## ⚙️ Setup & Usage

### 🐍 1. Local Development

**Install dependencies:**

```bash
pip install -r requirements.txt
```

**Run Flask server:**

```bash
cd src
flask run
```

By default, runs on `http://127.0.0.1:5001`.

---

### 🐳 2. Run with Docker

**Build the Docker image:**

```bash
docker build -t osheet-backend .
```

**Run with Docker Compose:**

```bash
docker-compose up --build
```

**App will be accessible at:**  
`http://localhost:8000`

---

## 🔒 Notes

- Uploaded images are stored as base64 strings in the SQLite DB.
- The database is located at `src/instance/osheet.db` by default.
- Make sure to persist the `instance/` folder in production if needed.

---

## 📜 License

MIT License
