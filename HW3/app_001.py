from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/user.db'
app.config['SECRET_KEY'] = 'e2b0d026f6dfd31f6051b33f5ca642dcc4fbc0a8aaf6fdc8eb0d8f7292569030'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    def __repr__(self):
        return f'first_name({self.first_name}, {self.last_name})'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    firstname = request.form.get('firstname')
    lastname = request.form.get('lastname')
    email = request.form.get('email')
    password = request.form.get('password')

    hashed_password = generate_password_hash(password, method='pbkdf2:sha1', salt_length=8)

    new_user = User(firstname=firstname, lastname=lastname, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return render_template('welcome.html', firstname=firstname, lastname=lastname)

@app.route('/back')
def back():
    return redirect(url_for('index'))

if __name__ == '__main__':
     with app.app_context():
        db.create_all()
        app.run(debug=True)

