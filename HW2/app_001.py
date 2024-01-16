from flask import Flask, render_template, request, redirect, url_for, make_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/welcome', methods=['POST'])
def welcome():
    name = request.form.get('name')
    email = request.form.get('email')

    response = make_response(render_template('welcome.html', name=name))
    response.set_cookie('user_data', f'{name}:{email}')

    return response

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('index')))
    response.delete_cookie('user_data')

    return response

if __name__ == '__main__':
    app.run(debug=True)
