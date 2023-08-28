from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from my_app.api.views import todo

login_manager = LoginManager()

SECRET_KEY = "some secret key"
app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():
    login_manager.init_app(app)
    app.register_blueprint(todo)

    from my_app.api.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    @app.route('/index')
    def home():
        return "Hello there, Are you excited"

    db.create_all()