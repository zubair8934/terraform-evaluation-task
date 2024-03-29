from flask import Flask, render_template, request, redirect, url_for
import pymysql
import os


app = Flask(__name__)

hostname = "hostname_here"
user = "username_here"
password = "password_here"
database = "database_name_here"

db = pymysql.connections.Connection(
    host=hostname,
    user=user,
    password=password,
    database=database,
    cursorclass=pymysql.cursors.DictCursor
)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            with db.cursor() as cursor:
                sql = "SELECT * FROM users WHERE username = %s AND password = %s"
                cursor.execute(sql, (username, password))
                user = cursor.fetchone()
                cursor.close()
                if user:
                    return redirect(url_for('home'))
                else:
                    return render_template('login.html', error='Invalid username or password')
        except Exception as e:
            return str(e)
    
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            with db.cursor() as cursor:
                sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(sql, (username, password))
                db.commit()
                cursor.close()
        except Exception as e:
            return str(e)

        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/home')
def home():
    images = [
        {"url": "static/images/image1.jpg", "alt": "Product 1", "description": "Product 1 Description"},
        {"url": "static/images/image2.jpg", "alt": "Product 2", "description": "Product 2 Description"},
        {"url": "static/images/image3.jpg", "alt": "Product 3", "description": "Product 3 Description"},
        {"url": "static/images/image4.jpg", "alt": "Product 4", "description": "Product 4 Description"},
        {"url": "static/images/image5.jpg", "alt": "Product 5", "description": "Product 5 Description"},
        {"url": "static/images/image6.jpg", "alt": "Product 6", "description": "Product 6 Description"},
    ]
    return render_template('index.html', images=images)



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

