from flask import Flask, render_template, redirect, request, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'secret_key#123456789'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        session['username'] = username
        return redirect(url_for('user_profile'))
    else:
        if "username" in session:
            return redirect(url_for('user_profile'))
        return render_template('login.html')


@app.route('/user_profile')
def user_profile():
    if ("username" in session):
        username = session['username']
        username = username.capitalize()
        return render_template('user_profile.html', username=username)
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if ("username" in session):
        session.pop('username', None)
        flash("You have been logged out!", "info")
    return redirect(url_for('login'))


if (__name__ == '__main__'):
    app.run(debug=True)
