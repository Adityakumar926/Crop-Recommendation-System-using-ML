from flask import Flask, request, render_template, redirect, url_for, session, flash
import numpy as np
import pickle
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
import os
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'adityakum.9430@gmail.com'
app.config['MAIL_PASSWORD'] = 'vnih ksau lbxf tuyx'

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    reset_token = db.Column(db.String(256), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

model = pickle.load(open('model.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))
mx = pickle.load(open('minmaxscaler.pkl', 'rb'))

@app.route('/')
def home():
    return redirect(url_for('register'))

# @app.route('/make_admin/<username>')
# def make_admin(username):
#     user = User.query.filter_by(username=username).first()
#     if user:
#         user.is_admin = True
#         db.session.commit()
#         return f"{username} is now an admin!"
#     return "User not found."

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        
        if User.query.count() == 0:
            new_user = User(username=username, email=email, password_hash=hashed_password, is_admin=True)
        else:
            new_user = User(username=username, email=email, password_hash=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('login'))

        session['username'] = username
        session['is_admin'] = user.is_admin 

        flash('Logged in successfully!', 'success')
        
        if user.is_admin:
            return redirect(url_for('admin'))  
        else:
            return redirect(url_for('index')) 

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('is_admin', None)
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_password_hash(email)
            user.reset_token = token
            db.session.commit()
            reset_link = url_for('reset_password', token=token, _external=True)
            msg = Message('Password Reset', sender='your_email@gmail.com', recipients=[email])
            msg.body = f'Click here to reset your password: {reset_link}'
            mail.send(msg)
            flash('Check your email for the reset link!', 'info')
        return redirect(url_for('login'))
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    if not user:
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form['password']
        user.password_hash = generate_password_hash(new_password)
        user.reset_token = None
        db.session.commit()
        flash('Password reset successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('reset_password.html')

@app.route('/index')
def index():
    if 'username' not in session:
        flash('You must log in to access this feature.', 'danger')
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/admin')
def admin():
    if 'username' not in session or not session.get('is_admin'):
        flash('You must be an admin to access this page.', 'danger')
        return redirect(url_for('login'))
    
    users = User.query.all() 
    return render_template('Admin.html', users=users)

@app.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    if 'username' not in session or not session.get('is_admin'):
        flash('You must be an admin to access this page.', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(user_id)
    
    if user:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully.', 'success')
    else:
        flash('User not found.', 'danger')

    return redirect(url_for('admin'))

@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        flash('You must log in to access this feature.', 'danger')
        return redirect(url_for('login'))
    
    feature_list = [request.form[key] for key in ['Nitrogen', 'Phosphorus', 'Potassium', 'Temperature', 'Humidity', 'pH', 'Rainfall']]
    single_pred = np.array(feature_list).reshape(1, -1)
    
    mx_features = mx.transform(single_pred)
    sc_mx_features = sc.transform(mx_features)
    prediction = model.predict(sc_mx_features)
    
    crop_dict = {1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
                 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
                 14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
                 19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"}
    
    result = crop_dict.get(prediction[0], "Sorry, we could not determine the best crop.")
    return render_template('index.html', result=result)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
