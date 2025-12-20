from flask import Flask, request, jsonify, send_from_directory, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import bcrypt
from db import mysql, init_db

# -------------------------------
# App setup
# -------------------------------
app = Flask(__name__, 
            static_folder=os.path.join(os.getcwd(), "..", "frontend"), 
            static_url_path="")

# IMPORTANT: Secret key is required for session management
app.secret_key = os.getenv('SECRET_KEY', 'kitabghar_fallback_key_123')

CORS(app)

# -------------------------------
# Database init
# -------------------------------
init_db(app)

# -------------------------------
# Upload folder config
# -------------------------------
UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# -------------------------------
# Frontend Routes
# -------------------------------

@app.route("/")
def serve_index():
    """Serves the main login page from the frontend folder"""
    return send_from_directory(app.static_folder, "login.html")

@app.route("/<path:path>")
def serve_static(path):
    """Serves other static files like index.html, css/style.css, etc."""
    return send_from_directory(app.static_folder, path)

# -------------------------------
# API Routes (Backend Logic)
# -------------------------------

@app.route("/health")
def health_check():
    return "KitabGhar Backend is running!"

# Register
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role", "user")

    if not username or not password:
        return jsonify({"message": "Username and Password required"}), 400

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO users(username, password, role) VALUES(%s, %s, %s)",
        (username, hashed_pw, role)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "User Registered Successfully"})

# Login
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    cur = mysql.connection.cursor()
    cur.execute("SELECT password, role FROM users WHERE username=%s", (username,))
    user = cur.fetchone()
    cur.close()

    if not user:
        return jsonify({"message": "User Not Found"}), 404

    stored_password = user[0].encode()

    if bcrypt.checkpw(password.encode(), stored_password):
        # Store user info in session
        session['logged_in'] = True
        session['username'] = username
        session['role'] = user[1]
        
        return jsonify({"message": "Login Successful", "role": user[1]})
    else:
        return jsonify({"message": "Invalid Password"}), 401

# Logout
@app.route("/logout", methods=["POST", "GET"])
def logout():
    """Clears the server-side session"""
    session.clear()
    return jsonify({"message": "Logout Successful"}), 200

# Upload ebook
@app.route("/upload", methods=["POST"])
def upload_ebook():
    title = request.form.get("title")
    author = request.form.get("author")
    category = request.form.get("category")
    file = request.files.get("file")

    if not file:
        return jsonify({"message": "No file uploaded"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO ebooks(title, author, category, file_path) VALUES(%s, %s, %s, %s)",
        (title, author, category, filename)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "E-Book Uploaded Successfully"})

# Get ebooks (Updated to include ID for deletion)
@app.route("/ebooks", methods=["GET"])
def get_ebooks():
    cur = mysql.connection.cursor()
    # Now selecting ID so frontend knows which book to delete
    cur.execute("SELECT id, title, author, category, file_path FROM ebooks")
    rows = cur.fetchall()
    cur.close()

    ebooks = []
    for row in rows:
        ebooks.append({
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "category": row[3],
            "file": row[4]
        })

    return jsonify(ebooks)

# --- NEW DELETE ROUTE ---
@app.route("/delete/<int:book_id>", methods=["DELETE"])
def delete_ebook(book_id):
    """Deletes book record from DB and actual file from storage"""
    cur = mysql.connection.cursor()
    
    # Get filename first to remove it from disk
    cur.execute("SELECT file_path FROM ebooks WHERE id = %s", (book_id,))
    book = cur.fetchone()
    
    if book:
        filename = book[0]
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        
        # Remove file from uploads folder
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Error deleting file: {e}")

        # Remove record from database
        cur.execute("DELETE FROM ebooks WHERE id = %s", (book_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({"message": "Book deleted successfully"}), 200
    
    cur.close()
    return jsonify({"message": "Book not found"}), 404

# Download file
@app.route("/uploads/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)