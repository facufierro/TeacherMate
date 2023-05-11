from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # initialize database
app = Flask(__name__)
app.secret_key = 'development key'
# path to database at the same level as app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teachermate.db'
# silence the deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password


class Student(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email


class Class(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    students = db.relationship('Student', backref='class', lazy=True)

    def __init__(self, description):
        self.description = description


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if (email == "" or password == ""):
            flash("Please fill in all fields!", "error")
            return redirect(url_for('login'))

        elif (User.query.filter_by(email=email).first() is None):
            flash("Incorrect email or password.", "error")
            return redirect(url_for('login'))

        elif (User.query.filter_by(email=email).first().password != password):
            flash("Incorrect email or password.", "error")
            return redirect(url_for('login'))

        else:
            session['email'] = email
            return redirect(url_for('home'))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('home'))


@app.route('/users/create', methods=['POST', 'GET'])
def user_create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if (name == "" or email == "" or password1 == "" or password2 == ""):
            flash("Please fill in all fields!", "error")
            return redirect(url_for('register'))

        elif (User.query.filter_by(email=email).first() is not None):
            flash("Email already registered!", "error")
            return redirect(url_for('register'))

        elif (password1 != password2):
            flash("Passwords do not match!", "error")
            return redirect(url_for('register'))

        else:
            new_user = User(name, email, password1)
            db.session.add(new_user)
            db.session.commit()
            flash("You have been registered!", "success")
            return redirect(url_for('login'))

    else:
        return render_template('users/create.html')


@app.route('/users/detail')
def user_detail():
    if 'email' not in session:
        flash("Please login first!", "info")
        return redirect(url_for('login'))
    else:
        user_name = User.query.filter_by(email=session['email']).first().name
        user_name = user_name.capitalize()
        return render_template('users/detail.html', user_name=user_name)


with app.app_context():
    db.create_all()

if (__name__ == '__main__'):
    app.run(debug=True)
