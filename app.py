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


class Area(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    description = db.Column(db.String(100))

    def __init__(self, description):
        self.description = description


class Activity (db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    area_id = db.Column(db.Integer, db.ForeignKey('area.id'), nullable=False)
    area = db.relationship('Area', backref=db.backref('activities', lazy=True))

    def __init__(self, description, area_id):
        self.description = description
        self.area_id = area_id


class Level(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    description = db.Column(db.String(100))

    def __init__(self, description):
        self.description = description


class Goal(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    description = db.Column(db.String(100))

    def __init__(self, description):
        self.description = description


class Grades(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    description = db.Column(db.String(100))
    lesson_id = db.Column(db.Integer, db.ForeignKey(
        'lesson.id'), nullable=False)
    lesson = db.relationship('Lesson', backref=db.backref('grades', lazy=True))

    def __init__(self, description, lesson_id):
        self.description = description
        self.lesson_id = lesson_id


class Student(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))

    def __init__(self, name, surname, email, phone):
        self.name = name
        self.surname = surname
        self.email = email
        self.phone = phone


class Lesson(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    description = db.Column(db.String(100))
    introduction = db.Column(db.String(100))
    conclusion = db.Column(db.String(100))
    notes = db.Column(db.String(100))
    activity_id = db.Column(db.Integer, db.ForeignKey(
        'activity.id'), nullable=False)
    activity = db.relationship(
        'Activity', backref=db.backref('lessons', lazy=True))
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)
    level = db.relationship('Level', backref=db.backref('lessons', lazy=True))
    student_id = db.Column(db.Integer, db.ForeignKey(
        'student.id'), nullable=False)
    student = db.relationship(
        'Student', backref=db.backref('lessons', lazy=True))
    goal_id = db.Column(db.Integer, db.ForeignKey('goal.id'), nullable=False)
    goal = db.relationship('Goal', backref=db.backref('lessons', lazy=True))

    def __init__(self, date, description, introduction, conclusion, notes, activity_id, level_id, student_id, goal_id):
        self.date = date
        self.description = description
        self.introduction = introduction
        self.conclusion = conclusion
        self.notes = notes
        self.activity_id = activity_id
        self.level_id = level_id
        self.student_id = student_id
        self.goal_id = goal_id


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
