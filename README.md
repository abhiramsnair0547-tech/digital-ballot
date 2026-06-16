# Digital Ballot 🗳️

A secure web-based online voting system built with Python and Flask, 
featuring separate Admin and Voter modules with a clean UI.

## 📋 Features

### Voter Module
- Secure login and authentication
- View candidates and cast vote
- Duplicate vote prevention
- Vote success confirmation page

### Admin Module
- Admin login and dashboard
- Candidate registration and management
- Real-time vote monitoring
- View election results

## 🛠️ Tech Stack
| Category | Technology |
|---|---|
| Language | Python |
| Framework | Flask |
| Database | SQLite (via Flask SQLAlchemy) |
| Frontend | HTML · CSS |
| IDE | Visual Studio |

## 📁 Project Structure
digital-ballot/

│

├── app.py                  # Main Flask application

├── create_admin.py         # Admin account setup script

│

├── static/

│   ├── style.css           # Stylesheet

│   └── uploads/            # Candidate image uploads

│

└── templates/

├── base.html           # Base template

├── index.html          # Home page

├── login.html          # Voter login

├── voter.html          # Voter dashboard

├── vote.html           # Voting page

├── vote_success.html   # Vote confirmation

├── already_voted.html  # Duplicate vote page

├── results.html        # Results page

└── admin.html          # Admin dashboard

## 🚀 How to Run

### Prerequisites
- Python 3.x installed
- Flask installed

### Steps
1. Clone the repository:
https://github.com/abhiramsnair0547-tech/digital-ballot.git
2. Navigate to project folder:
cd digital-ballot
3. Install dependencies:
pip install flask flask-sqlalchemy
4. Set up admin account:
python create_admin.py
5. Run the application:
python app.py
6. Open browser at:
http://localhost:5000

## ⚠️ Known Issues
- Flash error messages on invalid actions currently 
  show as page refresh instead of inline error display
- Being improved in future updates

## 👤 Project Info
- **Type:** Mini Project — Semester 6
- **Role:** Team Lead & Lead Developer
- **Year:** 2024
- **Institution:** Ahalia School of Engineering 
  and Technology, Palakkad
- **University:** APJ Abdul Kalam Technological University
