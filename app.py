import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this for security

# Database Configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Image Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ------------------ DATABASE MODELS ------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed passwords
    is_admin = db.Column(db.Boolean, default=False)
    has_voted = db.Column(db.Boolean, default=False)

class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)  # Ensure unique candidate names
    votes = db.Column(db.Integer, default=0)
    image = db.Column(db.String(200), nullable=True)  # Stores image filename

# ------------------ HELPER FUNCTION ------------------

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ------------------ ROUTES ------------------

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['is_admin'] = user.is_admin
            return redirect(url_for('admin_dashboard') if user.is_admin else url_for('voter_dashboard'))
        
        flash("Invalid login credentials!", "danger")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/admin')
def admin_dashboard():
    if not session.get("is_admin"):
        return redirect(url_for("login"))

    user = User.query.get(session['user_id'])  # Get the logged-in admin user
    candidates = Candidate.query.all()
    voters = User.query.filter_by(is_admin=False).all()

    return render_template("admin.html", user=user, candidates=candidates, voters=voters)

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'user_id' not in session:
        flash("You must be logged in to vote.", "warning")
        return redirect(url_for('login'))

    user = User.query.get(session['user_id'])
    
    if user.has_voted:
        flash("You have already voted.", "danger")
        return redirect(url_for('already_voted'))

    candidates = Candidate.query.all()

    if request.method == 'POST':
        candidate_id = request.form.get('candidate')
        candidate = Candidate.query.get(candidate_id)
        
        if candidate:
            candidate.votes += 1
            user.has_voted = True
            db.session.commit()
            flash("Your vote has been recorded successfully!", "success")
            return redirect(url_for('vote_success'))

    return render_template('vote.html', candidates=candidates)

@app.route('/vote_success')
def vote_success():
    return render_template('vote_success.html')

@app.route('/already_voted')
def already_voted():
    return render_template('already_voted.html')

@app.route('/results')
def results():
    if not session.get('is_admin'):
        return "Access denied!"
    
    candidates = Candidate.query.all()
    return render_template('results.html', candidates=candidates)

@app.route('/add_candidate', methods=['POST'])
def add_candidate():
    """Admin can add candidates with images"""
    if not session.get('is_admin'):
        return redirect(url_for('home'))

    name = request.form.get('name')
    image = request.files.get('image')  # Get image file from the form

    # Ensure candidate name is unique
    existing_candidate = Candidate.query.filter_by(name=name).first()
    if existing_candidate:
        flash("Candidate name already exists!", "danger")
        return redirect(url_for('admin_dashboard'))

    if name and image and allowed_file(image.filename):
        # Generate a unique filename
        filename = f"{uuid.uuid4().hex}_{secure_filename(image.filename)}"
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        # Save candidate to database
        new_candidate = Candidate(name=name, image=filename)
        db.session.add(new_candidate)
        db.session.commit()
        flash("Candidate added successfully!", "success")
    else:
        flash("Invalid file format! Please upload a valid image.", "danger")
    
    return redirect(url_for('admin_dashboard'))

@app.route('/add_voter', methods=['POST'])
def add_voter():
    if not session.get('is_admin'):
        return redirect(url_for('home'))

    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            hashed_password = generate_password_hash(password)
            new_voter = User(username=username, password=hashed_password, is_admin=False)
            db.session.add(new_voter)
            db.session.commit()
            flash("Voter registered successfully!", "success")
        else:
            flash("Username already exists!", "danger")
    
    return redirect(url_for('admin_dashboard'))

@app.route('/voter_dashboard')
def voter_dashboard():
    if not session.get('user_id') or session.get('is_admin'):
        return redirect(url_for('login'))
    
    candidates = Candidate.query.all()
    return render_template('voter.html', candidates=candidates)

# ------------------ DATABASE INITIALIZATION ------------------

with app.app_context():
    db.create_all()
    # Ensure an admin exists
    if not User.query.filter_by(is_admin=True).first():
        admin = User(username="admin", password=generate_password_hash("admin123"), is_admin=True)
        db.session.add(admin)
        db.session.commit()

# ------------------ RUNNING THE APP ------------------

if __name__ == '__main__':
    app.run(debug=True)
