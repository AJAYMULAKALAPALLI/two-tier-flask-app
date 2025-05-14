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
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configure MySQL to connect to RDS
app.config['MYSQL_HOST'] = 'database-1.cb0a20044fec.us-east-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'  # Default RDS admin user
app.config['MYSQL_PASSWORD'] = 'Cprime2003'
app.config['MYSQL_DB'] = 'message_db'  # Will be created if doesn't exist
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Initialize MySQL
mysql = MySQL(app)

def initialize_database():
    """Create database and table if they don't exist"""
    try:
        # First connect without specifying a database
        conn = mysql.connection
        cur = conn.cursor()
        
        # Create database if not exists
        cur.execute("CREATE DATABASE IF NOT EXISTS message_db")
        conn.commit()
        
        # Now connect to the specific database
        cur.execute("USE message_db")
        
        # Create table if not exists
        cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT
        )
        """)
        conn.commit()
        cur.close()
        print("Database and table initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise e  # Re-raise the exception to see the full error

@app.before_first_request
def before_first_request():
    """Initialize database before first request"""
    initialize_database()

@app.route('/')
def hello():
    try:
        cur = mysql.connection.cursor()
        cur.execute('USE message_db')
        cur.execute('SELECT message FROM messages')
        messages = cur.fetchall()
        cur.close()
        return render_template('index.html', messages=messages)
    except Exception as e:
        return f"Error fetching messages: {str(e)}", 500

@app.route('/submit', methods=['POST'])
def submit():
    try:
        new_message = request.form.get('new_message')
        if not new_message:
            return "Message cannot be empty", 400
            
        cur = mysql.connection.cursor()
        cur.execute('USE message_db')
        cur.execute('INSERT INTO messages (message) VALUES (%s)', (new_message,))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('hello'))
    except Exception as e:
        return f"Error submitting message: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
