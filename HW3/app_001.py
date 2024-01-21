
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, url_for, redirect, flash
from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length, Email
from models_001 import User, db
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/user.db'
app.config['SECRET_KEY'] = 'e2b0d026f6dfd31f6051b33f5ca642dcc4fbc0a8aaf6fdc8eb0d8f7292569030'
csrf = CSRFProtect(app)

db.init_app(app)


@app.route('/')
def index():
    return 'Для запуска формы регистрации введите в браузере /login'

@app.route('/login/', methods=['GET', 'POST'])
@csrf.exempt
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        lastname = form.lastname.data
        email = form.email.data
        password = form.password.data

        hashed_password = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)

        new_user = User(firstname=firstname, lastname=lastname, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Пользователь успешно добавлен!', 'success')
        return redirect(url_for('login'))
    return render_template('login.html', form=form)


class LoginForm(FlaskForm):
    firstname = StringField('Имя', validators=[DataRequired()])
    lastname = StringField('Фамилия', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

