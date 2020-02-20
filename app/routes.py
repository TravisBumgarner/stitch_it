import os
from app import app
from flask import render_template, flash, redirect, request
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Travis'}
    return render_template('index.html', title='Home', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        print(os.path.abspath(__file__))
        f.save(os.path.join('uploads', f.filename))
        return render_template(
            "success.html",
            name = f.filename,
            results = '<div style="width: 100px; height: 100px; background-color: red;"></div>'
        )  