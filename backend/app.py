from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import bcrypt

from db import mysql, init_db

# -------------------------------
# App setup
# -------------------------------
app = Flask(__name__)
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
# Home route
# -------------------------------
@app.route("/")
def home():
    return "KitabGhar Backend Connected to MySQL"

# -------------------------------
# Register
# -------------------------------
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]
    role = data["role"]

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    cur = mysql.connection.cursor()
    cur.execute(
        "INSERT INTO users(username, password, role) VALUES(%s, %s, %s)",
        (username, hashed_pw, role)
    )
    mysql.connection.commit()
    cur.close()

    return jsonify({"message": "User Registered Successfully"})

# -------------------------------
# Login
# -------------------------------
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    cur = mysql.connection.cursor()
    cur.execute("SELECT password, role FROM users WHERE username=%s", (username,))
    user = cur.fetchone()
    cur.close()

    if not user:
        return jsonify({"message": "User Not Found"}), 404

    stored_password = user[0].encode()

    if bcrypt.checkpw(password.encode(), stored_password):
        return jsonify({"message": "Login Successful", "role": user[1]})
    else:
        return jsonify({"message": "Invalid Password"}), 401

# -------------------------------
# Upload ebook
# -------------------------------
@app.route("/upload", methods=["POST"])
def upload_ebook():
    title = request.form["title"]
    author = request.form["author"]
    category = request.form["category"]
    file = request.files["file"]

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

# -------------------------------
# Get ebooks
# -------------------------------
@app.route("/ebooks", methods=["GET"])
def get_ebooks():
    cur = mysql.connection.cursor()
    cur.execute("SELECT title, author, category, file_path FROM ebooks")
    rows = cur.fetchall()
    cur.close()

    ebooks = []
    for row in rows:
        ebooks.append({
            "title": row[0],
            "author": row[1],
            "category": row[2],
            "file": row[3]
        })

    return jsonify(ebooks)

# -------------------------------
# Download file
# -------------------------------
@app.route("/uploads/<filename>")
def download_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)
