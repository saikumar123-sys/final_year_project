from flask import Flask, render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
from extensions import db, login_manager

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your_secret_key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carbon_credit.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Upload configuration
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', 'documents')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
migrate = Migrate(app, db)

from models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from routes import *

from werkzeug.security import generate_password_hash
from models import User

def create_default_admin():
    admin = User.query.filter_by(email="admin@gmail.com").first()

    if not admin:
        admin = User(
            username="admin",
            email="admin@gmail.com",
            password=generate_password_hash("admin@123"),
            role="admin",
            is_approved=True,
            is_suspended=False,
            wallet_address="ADMIN_WALLET",
            private_key="ADMIN_PRIVATE_KEY"
        )

        db.session.add(admin)
        db.session.commit()
        print("Default Admin Created → admin@gmail.com / admin@123")
    else:
        print("Admin already exists")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_default_admin()   # ← IMPORTANT LINE
    app.run(debug=True)

