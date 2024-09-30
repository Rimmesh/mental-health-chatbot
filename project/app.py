from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
import pickle
import os
from werkzeug.security import generate_password_hash, check_password_hash
import logging
from chatbot import predict_sentiment, get_response

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

# Set the path for the SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'instance', 'database.db')

# Create the instance directory if it does not exist
if not os.path.exists(os.path.join(basedir, 'instance')):
    os.makedirs(os.path.join(basedir, 'instance'))

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



#database

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class SubEmail(db.Model):
    idSub = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, emailSub):
        self.emailSub = emailSub

with app.app_context():
    db.create_all()

def save_email_to_db(emailSub):
    new_email = SubEmail(emailSub=emailSub)
    db.session.add(new_email)
    db.session.commit()

def save_user_to_db(username, email, password):
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()





# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    emailSub = data.get('email')
    if emailSub:
        save_email_to_db(emailSub)
        return jsonify({'message': 'Subscription successful'}), 200
    return jsonify({'message': 'Subscription failed'}), 400

@app.route('/debug-emails')
def debug_emails():
    emails = SubEmail.query.all()
    email_list = [email.emailSub for email in emails]
    return jsonify(email_list), 200

@app.route('/is_logged_in', methods=['GET'])
def is_logged_in():
    if 'user' in session:
        return jsonify({'logged_in': True}), 200
    return jsonify({'logged_in': False}), 200

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    hashed_password = generate_password_hash(password)

    app.logger.info(f"Attempting to register user: username={username}, email={email}")

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        app.logger.warning(f"User with email {email} already exists.")
        return jsonify({"status": "user already exists"}), 400

    try:
        save_user_to_db(username, email, hashed_password)
        app.logger.info(f"User {username} added to the database.")
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error occurred while registering user: {str(e)}")
        return jsonify({"status": "registration failed", "error": str(e)}), 500

    user = User.query.filter_by(email=email).first()
    if user:
        app.logger.info(f"User {user.username} registered successfully with email {user.email}")
        session['user'] = user.id
        return jsonify({"status": "success"}), 200
    else:
        app.logger.error("User registration failed.")
        return jsonify({"status": "registration failed"}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):
        session['user'] = user.id
        return jsonify({"status": "success"}), 200
    elif user:
        return jsonify({"status": "incorrect password"}), 400
    else:
        return jsonify({"status": "user not found"}), 404

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/check-login-status')
def check_login_status():
    if 'user' in session:
        return jsonify(True)
    else:
        return jsonify(False)



#chatbot

@app.route('/chatbot')
def chatbot():
    if 'user' in session:
        return render_template('chatbot.html')
    else:
        return redirect(url_for('home'))

@app.route('/chatbot/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    user_message = data.get('message')
    predicted_label = predict_sentiment(user_message)
    response = get_response(predicted_label)
    return jsonify({'answer': response})




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, ''), filename)

if __name__ == '__main__':
    app.run(debug=True , port=5001)
