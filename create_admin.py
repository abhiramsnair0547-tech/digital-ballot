from app import db, User
from werkzeug.security import generate_password_hash

# Initialize database context
with db.session.begin():
    # Create admin user
    admin_user = User(username="admin", password=generate_password_hash("admin123"), is_admin=True)
    db.session.add(admin_user)

print("✅ Admin user created successfully!")
