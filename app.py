from flask import Flask, url_for
from flask import Flask, flash, redirect, render_template, request, session, abort
import os


#  the below code creates an instance of the app

app = Flask(__name__)

# these are the routes which set out what each page on the webapp will do
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Did it work???"

#
# @app.route("/login")
# def login():
#     return render_template("login.html")


@app.route('/login', methods=['GET','POST'])
def do_admin_login():
    if request.form['password'] == 'password' and request.form['username'] == 'admin':
        # session['logged_in'] = True
        return redirect(url_for('welcome'))
    else:
        flash('wrong password!')
        return home()

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'password':
            attempt = int(session.get('attempt'))
            if attempt == 2:
                flash("This is your last chance")
                # attempt += 1
                # session['attempt'] = attempt
            if attempt == 3:
                flash('You made too many incorrect login attempts. Please contact an administrator')
                abort(404)
            else:
                attempt += 1
                session['attempt'] = attempt
                error = 'Invalid Credentials. Please try again'
        else:
            session['logged_in'] = True
            flash('You were logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/welcome")
def welcome():
    return render_template("welcome.html")


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
