# import os
# from flask import Flask, render_template, request, redirect, url_for
# from flask_mysqldb import MySQL

# app = Flask(__name__)

# # Configure MySQL from environment variables
# app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
# app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'default_user')
# app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'default_password')
# app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'default_db')

# # Initialize MySQL
# mysql = MySQL(app)

# @app.route('/')
# def hello():
#     cur = mysql.connection.cursor()
#     cur.execute('SELECT message FROM messages')
#     messages = cur.fetchall()
#     cur.close()
#     return render_template('index.html', messages=messages)

# @app.route('/submit', methods=['POST'])
# def submit():
#     new_message = request.form.get('new_message')
#     cur = mysql.connection.cursor()
#     cur.execute('INSERT INTO messages (message) VALUES (%s)', [new_message])
#     mysql.connection.commit()
#     cur.close()
#     return redirect(url_for('hello'))

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

import os
from flask import Flask, render_template, request, redirect, url_for
import MySQLdb

app = Flask(__name__)

def get_db_connection(use_message_db=False):
    """Create a database connection"""
    kwargs = {
        'host': 'database-1.cb0a20044fec.us-east-2.rds.amazonaws.com',
        'user': 'admin',
        'password': 'Cprime2003',
    }
    if use_message_db:
        kwargs['db'] = 'message_db'
    return MySQLdb.connect(**kwargs)

def initialize_database():
    """Create database and table if they don't exist"""
    try:
        # First connect without specifying a database
        conn = get_db_connection(use_message_db=False)
        cur = conn.cursor()
        
        # Create database if not exists
        cur.execute("CREATE DATABASE IF NOT EXISTS message_db")
        conn.commit()
        conn.select_db('message_db')  # Switch to the message_db database
        
        # Now create the table
        cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT
        )
        """)
        conn.commit()
        cur.close()
        conn.close()
        print("Database and table initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise

# Initialize the database when the application starts
with app.app_context():
    initialize_database()

@app.route('/')
def hello():
    try:
        conn = get_db_connection(use_message_db=True)
        cur = conn.cursor()
        cur.execute('SELECT message FROM messages')
        messages = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('index.html', messages=messages)
    except Exception as e:
        return f"Error fetching messages: {str(e)}", 500

@app.route('/submit', methods=['POST'])
def submit():
    try:
        new_message = request.form.get('new_message')
        if not new_message:
            return "Message cannot be empty", 400
            
        conn = get_db_connection(use_message_db=True)
        cur = conn.cursor()
        cur.execute('INSERT INTO messages (message) VALUES (%s)', (new_message,))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('hello'))
    except Exception as e:
        return f"Error submitting message: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
