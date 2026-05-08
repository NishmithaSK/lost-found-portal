from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# CREATE DATABASE

conn = sqlite3.connect('lostfound.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS reports (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    status TEXT,
    location TEXT,
    contact TEXT

)
''')

conn.commit()
conn.close()


# HOME PAGE

@app.route('/')
def home():
    return render_template('index.html')


# SUBMIT REPORT

@app.route('/submit', methods=['POST'])
def submit():

    item_name = request.form['item_name']
    status = request.form['status']
    location = request.form['location']
    contact = request.form['contact']

    conn = sqlite3.connect('lostfound.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO reports
        (item_name, status, location, contact)

        VALUES (?, ?, ?, ?)
        ''',

        (item_name, status, location, contact)
    )

    conn.commit()
    conn.close()

    return redirect('/reports')


# REPORTS PAGE

@app.route('/reports')
def reports():

    conn = sqlite3.connect('lostfound.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM reports')

    data = cursor.fetchall()

    conn.close()

    return render_template(
        'reports.html',
        reports=data
    )


if __name__ == '__main__':
    app.run(debug=True)