import os
from flask_mysqldb import MySQL
from dotenv import load_dotenv

load_dotenv() # This loads the variables from your .env file

mysql = MySQL()

def init_db(app):
    # These will be pulled from your .env file locally 
    # and from "Environment Variables" on Render later
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.config['MYSQL_PORT'] = int(os.getenv('MYSQL_PORT', 3306))
    
    mysql.init_app(app)