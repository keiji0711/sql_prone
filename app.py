from flask import Flask, request, redirect, render_template
import sqlite3
import os

app = Flask(__name__)
DATABASE = 'database.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT,
                            email TEXT
                        );''')

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users;")
    users = cursor.fetchall()
    conn.close()
    return render_template('index.html', users=users)

@app.route('/add', methods=['POST'])
def add_user():
    username = request.form['username'] # fake
    email = request.form['email'] # '); DELETE FROM users;--

    query = f"INSERT INTO users (username, email) VALUES ('{username}', '{email}');"

    #query = f"INSERT INTO users (username, email) VALUES (?,?);" #secure
    


    conn = sqlite3.connect(DATABASE)
    #conn.execute(query,(username,email))  #secure
    conn.executescript(query)
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<id>')
def delete_user(id):
    query = f"DELETE FROM users WHERE id = {id};"

    conn = sqlite3.connect(DATABASE)
    conn.execute(query)
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/update/<id>', methods=['POST'])
def update_user(id):
    username = request.form['username']
    email = request.form['email']

    query = "UPDATE users SET username = ?, email = ? WHERE id = ?"
    conn = sqlite3.connect(DATABASE)
    conn.execute(query, (username, email, id))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
    app.run(debug=True, host = '0.0.0.0', port = 5000)
