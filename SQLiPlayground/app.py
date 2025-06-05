import os
from flask import Flask, render_template, request, redirect, session
import mysql.connector
from mysql.connector import Error
import time
time.sleep(10)  # Add this near the top of your file


app = Flask(__name__)
app.secret_key = 'debug-secret'

MYSQL_CONFIG = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', 'root'),
    'database': os.getenv('MYSQL_DB', 'lab_db')
}

def get_db_connection():
    return mysql.connector.connect(**MYSQL_CONFIG)

def get_cursor(conn):
    return conn.cursor(dictionary=True)

#
    return mysql.connector.connect(**MYSQL_CONFIG)


@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    if request.method == 'POST':
        content = request.form['content']
        try:
            conn = get_db_connection()
            c = get_cursor(conn)
            query = f"INSERT INTO comments (content) VALUES ('{content}')"
            print(f"[DEBUG] Inserting comment with query: {query}")
            c.execute(query)
            conn.commit()
        except Exception as e:
            message = f"Error: {e}"
        finally:
            conn.close()

    conn = get_db_connection()
    c = get_cursor(conn)
    c.execute("SELECT * FROM comments")
    comments = c.fetchall()
    conn.close()
    return render_template('index.html', comments=comments, message=message)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        print(f"[DEBUG] Login SQL: {query}")
        conn = get_db_connection()
        c = get_cursor(conn)
        try:
            c.execute(query)
            user = c.fetchone()
            print(f"[DEBUG] Query Result: {user}")
            if user:
                session['user'] = user['username']
                return redirect('/dashboard')
            else:
                error = "Login failed"
        except Exception as e:
            error = f"Error: {e}"
        finally:
            conn.close()
    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', username=session['user'])

@app.route('/profile')
def profile():
    username = session.get('user', 'Guest')
    email = f"{username}@example.com"
    return render_template("profile.html", username=username, email=email)

@app.route('/stored', methods=['GET', 'POST'])
def stored_injection():
    message = ''
    if request.method == 'POST':
        content = request.form['content']
        try:
            conn = get_db_connection()
            c = get_cursor(conn)
            query = f"INSERT INTO comments (content) VALUES ('{content}')"
            print(f"[DEBUG - STORED] Inserting comment: {query}")
            c.execute(query)
            conn.commit()
        except Exception as e:
            message = f"Error: {e}"
        finally:
            conn.close()

    conn = get_db_connection()
    c = get_cursor(conn)
    c.execute("SELECT * FROM comments")
    comments = c.fetchall()
    conn.close()
    return render_template('stored.html', comments=comments, message=message)

@app.route('/blind', methods=['GET', 'POST'])
def blind_sqli():
    result = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        try:
            conn = get_db_connection()
            c = get_cursor(conn)
            query = f"SELECT * FROM users WHERE username = '{username}'"
            print(f"[DEBUG - BLIND] Query: {query}")
            start = time.time()
            c.execute(query)
            user = c.fetchone()
            duration = time.time() - start
            print(f"[DEBUG] Query duration: {duration:.4f}s")
            if user:
                result = f"User found! (response time: {duration:.2f}s)"
            else:
                result = f"No such user. (response time: {duration:.2f}s)"
        except Exception as e:
            result = f"Error: {e}"
        finally:
            conn.close()
    return render_template('blind.html', result=result)

@app.route('/search')
def search():
    query_param = request.args.get('q', '')
    results = []
    error = ''
    try:
        conn = get_db_connection()
        c = get_cursor(conn)
        sql = f"SELECT * FROM users WHERE username LIKE '%{query_param}%'"
        print(f"[DEBUG] SQL Query: {sql}")
        c.execute(sql, multi=True)  # this will allow stacked queries
        results = c.fetchall()
    except Exception as e:
        error = f"Error: {e}"
    finally:
        conn.close()

    return render_template('search.html', results=results, q=query_param, error=error)


# Insecure IDOR: No access control
@app.route('/user-profile-insecure')
def user_profile_insecure():
    user_id = request.args.get('id')

    # ✅ Stop here if ID is missing or not digits
    if not user_id or not user_id.isdigit():
        return "<p>Invalid or missing user ID.</p>"

    try:
        conn = get_db_connection()
        c = get_cursor(conn)
        c.execute("SELECT id, username FROM users WHERE id = %s", (user_id,))
        user = c.fetchone()
        conn.close()
    except Exception as e:
        return f"<p>Error: {e}</p>"

    if user:
        return render_template("user_profile.html", user=user)
    return "<p>User not found.</p>"



@app.route('/api/user-info')
def api_user_info():
    user_id = request.args.get('id')
    conn = get_db_connection()
    c = get_cursor(conn)
    c.execute("SELECT id, username, email FROM users WHERE id = %s", (user_id,))
    user = c.fetchone()
    conn.close()

    if user:
        return user
    return {"error": "User not found"}, 404


# Secure version: only allow access to logged-in user's profile
@app.route('/user-profile-secure')
def user_profile_secure():
    if 'user' not in session:
        return redirect('/login')

    user_id = request.args.get('id', '')
    conn = get_db_connection()
    c = conn.cursor(dictionary=True)
    c.execute("SELECT id, username FROM users WHERE username = %s", (session['user'],))
    current_user = c.fetchone()
    conn.close()

    if str(current_user['id']) != user_id:
        return "<p>Access Denied.</p>"

    return render_template("user_profile.html", user=current_user)

@app.route('/api/user-info-secure')
def api_user_info_secure():
    if 'user' not in session:
        return {"error": "Login required"}, 401

    requested_id = request.args.get('id')
    conn = get_db_connection()
    c = get_cursor(conn)
    c.execute("SELECT id FROM users WHERE username = %s", (session['user'],))
    current_user = c.fetchone()
    conn.close()

    if str(current_user['id']) != requested_id:
        return {"error": "Access Denied"}, 403

    return current_user


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')



@app.route('/blind-boolean', methods=['GET', 'POST'])
def blind_boolean():
    result = ''
    if request.method == 'POST':
        username = request.form.get('username', '')
        try:
            conn = get_db_connection()
            c = get_cursor(conn)
            query = f"SELECT * FROM users WHERE username = '{username}'"
            print(f"[DEBUG - BOOLEAN BLIND] Query: {query}")
            c.execute(query)
            user = c.fetchone()
            if user:
                result = "User exists!"
            else:
                result = "User does not exist."
        except Exception as e:
            result = f"Error: {e}"
        finally:
            conn.close()
    return render_template('blind_boolean.html', result=result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')