from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField
from wtforms.validators import DataRequired, Email, ValidationError

class NameForm(FlaskForm):
    name = StringField('What is your name', validators=[DataRequired()])
    email = EmailField('What is your UofT Email address', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'HARDTOGUESS'
moment = Moment(app)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    print(session.get('name'))
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_info = session.get('info')
        if old_info and old_info['name'] is not None and old_info['name'] != form.name.data:
            flash('Looks like you have changed your name!')
        if old_info and old_info['email'] is not None and old_info['email'] != form.email.data:
            flash('Looks like you have changed your email!')
        session['info'] = {
            'name': form.name.data,
            'email': form.email.data,
        }
        return redirect(url_for('index'))
    return render_template('index.html', form=form, formInfo=session.get('info'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time=datetime.utcnow())

if __name__ == '__main__':
    app.run()
