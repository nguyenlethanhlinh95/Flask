import flask_login
from flask import Flask, render_template, request
from flask_login import LoginManager, login_required, current_user, login_user, UserMixin, logout_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.secret_key = 'Thisissecrectkey'
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)  # SQL Achemy

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# silly user model
class User(flask_login.UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    username = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    join_date = db.Column(db.DateTime)


# callback to reload the user object
@login_manager.user_loader
def load_user(user_id):
    # 1. Fetch against the database a user by `id`
    # 2. Create a new object of `User` class and return it.
    u = User.query.get(user_id)
    return u


@app.route('/login', methods=['GET', 'POST'])
def login():
    # user = User.query.filter(User.username=='Linh').first()
    # login_user(user)
    # # load_user(user)
    # return '<h1>You are now logged in!</h1>'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter(db.and_(User.username == username, User.password == password)).first()
        if not user:
            return render_template('login.html')
        login_user(user)
        return render_template('home.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return '<h1>User are logout!</h1>'


@app.route('/')
def hello_world():
    return 'Hello world'


@app.route('/home')
@flask_login.login_required
def home():
    return render_template('home.html')


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'


if __name__ == '__main__':
    app.run(debug=True)
