# 📚 KitabGhar - Modern E-Book Library Management System

KitabGhar is a professional full-stack web application designed for digital library management. It features a modern, responsive "Dark Mode" UI, secure user authentication, and a robust backend for managing PDF e-books.

---

## 🚀 Key Features

### **User Side**
- **Secure Authentication:** User registration and login powered by `bcrypt` password hashing.
- **Modern Library Catalog:** A sleek, responsive grid view of all available e-books.
- **Instant Downloads:** One-click access to download PDF books directly from the server.
- **Session Management:** Secure logout functionality that clears both client-side and server-side data.

### **Admin Side**
- **Admin Dashboard:** Dedicated interface for library management.
- **Book Uploads:** Add new titles with metadata (Author, Category) and PDF file storage.
- **Management Tools:** View a live preview and delete books instantly from both the database and storage.

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3 (Glassmorphism UI), JavaScript (Vanilla ES6)
- **Backend:** Python, Flask, Flask-CORS, Flask-MySQLdb
- **Database:** MySQL (Hosted on **Aiven**)
- **Deployment:** GitHub & Render

---

## 📂 Project Structure

```text
KITABGHAR/
├── backend/
│   ├── app.py           # Flask server & API routes
│   ├── db.py            # MySQL database configuration
│   ├── uploads/         # Directory for stored PDF files
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── css/
│   │   └── style.css    # Modern Dark UI styling
│   ├── js/
│   │   └── script.js    # Frontend logic & API integration
│   ├── index.html       # User Library page
│   ├── admin.html       # Admin management page
│   ├── login.html       # Entry portal
│   └── register.html    # New user registration
└── Procfile             # Deployment config for Render
