from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime
from flask_cors import CORS 
import os
app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

class SurveyData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sleep_time = db.Column(db.String(5), nullable=False)
    wake_up_time = db.Column(db.String(5), nullable=False)
    
# Initialization of the database and creation of the default admin user
with app.app_context():
    db.create_all()

    # Check if the default admin user exists
    default_admin = User.query.filter_by(username='benaiah').first()
    if not default_admin:
        # Create the default admin user
        default_admin = User(username='benaiah', password=generate_password_hash('bena124'))
        db.session.add(default_admin)
        db.session.commit()

@app.route('/', methods=['GET', 'POST'])
def welcome():
    # Get the current time
    current_time = datetime.now().strftime('%H:%M')

    # Define different messages based on the time of the day
    if '05:00' <= current_time < '12:00':
        greeting = 'Good morning!'
    elif '12:00' <= current_time < '17:00':
        greeting = 'Good afternoon!'
    elif '17:00' <= current_time < '21:00':
        greeting = 'Good evening!'
    else:
        greeting = 'Good night!'

    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('welcome.html', greeting=greeting)

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        sleep_time = request.form['sleep_time']
        wake_up_time = request.form['wake_up_time']
        
        # Check if the entry was successfully added to the database
        try:
            new_entry = SurveyData(name=name, sleep_time=sleep_time, wake_up_time=wake_up_time)
            db.session.add(new_entry)
            db.session.commit()
            flash('Survey data submitted successfully!', 'success')
            
            
            return render_template('index.html', currentSlide=currentSlide)
        except:
            flash('Error occurred while submitting survey data.', 'danger')

    currentSlide = int(request.args.get('slide', 0))
    return render_template('index.html', currentSlide=currentSlide)


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Successful login
            session['admin_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('admin_login.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin_dashboard():
    admin_id = session.get('admin_id')

    if not admin_id:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('admin_login'))

    # Query the user based on admin_id
    user = User.query.get(admin_id)

    if not user:
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('index'))

    total_entries = SurveyData.query.count()

    if request.method == 'POST':
        action = request.form['action']
        if action == 'add_admin':
            username = request.form['username']
            password = request.form['password']
            new_admin = User(username=username, password=generate_password_hash(password))
            try:
                db.session.add(new_admin)
                db.session.commit()
                flash('Admin added successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            except:
                flash('Error occurred while adding admin.', 'danger')
        elif action == 'delete':
            entry_id = int(request.form['entry_id'])
            entry_to_delete = SurveyData.query.get(entry_id)
            try:
                db.session.delete(entry_to_delete)
                db.session.commit()
                flash('Entry deleted successfully!', 'success')
                return redirect(url_for('admin_dashboard'))
            except:
                flash('Error occurred while deleting entry.', 'danger')

    data = SurveyData.query.all()
    return render_template('admin.html', data=data, total_entries=total_entries)

if __name__ == '__main__':
#   backend_url = os.environ.get('BACKEND_URL', 'http://localhost:5000')  # Default for development
  app.run(host='0.0.0.0', port=5000, debug=False)
    
