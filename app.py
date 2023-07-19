from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy()
db.init_app(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        user_username = request.form['username']
        user_password = request.form['password']
        new_user = User(username=user_username, password=user_password)
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect("/users")
        except: 
            return 'There was an issue signing up'
    else:
        return render_template('Signup.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/contact')
def connect():
    return render_template('Contact.html')

@app.route('/service')
def service():
    return render_template('Service.html')

@app.route('/users', methods=['GET'])
def users():
    users = User.query.order_by(User.date_created).all()
    print(len(users))
    return render_template('users.html', users=users)



if (__name__ == "__main__"):
    app.run(debug=True)