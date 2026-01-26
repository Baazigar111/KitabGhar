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
│   └── Procfile         # Deployment config (located here)
├── frontend/
│   ├── css/
│   │   └── style.css    # Modern Dark UI styling
│   ├── js/
│   │   └── script.js    # Frontend logic & API integration
│   ├── index.html       # User Library page
│   ├── admin.html       # Admin management page
│   ├── login.html       # Entry portal
│   └── register.html    # New user registration
└── requirements.txt     # Python dependencies (located in root)

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/KitabGhar.git
cd KitabGhar

2️⃣ Setup Backend

Install the required dependencies from the root directory:

pip install -r requirements.txt

3️⃣ Database Configuration

Make sure your Aiven MySQL instance is running, then create the tables below:

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user'
);

CREATE TABLE ebooks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100),
    category VARCHAR(50),
    file_path VARCHAR(255)
);

4️⃣ Environment Variables

On your hosting platform (Render / Heroku), set the following environment variables:

MYSQL_HOST
MYSQL_USER
MYSQL_PASSWORD
MYSQL_DB
MYSQL_PORT
SECRET_KEY


🔐 SECRET_KEY → Any random long string

☁️ Deployment Note (Render)

When deploying to Render:

Connect your GitHub repository

Build Command

pip install -r requirements.txt


Start Command

gunicorn --chdir backend app:app


📌 This tells Render to:

Use requirements.txt from the root

Look for app.py inside the backend folder
