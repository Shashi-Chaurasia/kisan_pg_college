from models import db, Admin
from werkzeug.security import generate_password_hash
from app import create_app

# Create the app instance
app = create_app()


# Define a function to seed the admin user
def seed_admin():
    with app.app_context():  # Ensure you're working within the Flask app context
        # Check if the 'admin' user already exists
        admin = Admin.query.filter_by(username='admin').first()

        if not admin:
            # Create a new admin user with a hashed password using PBKDF2
            admin = Admin(
                username='admin',
                password=generate_password_hash('password123', method='pbkdf2:sha256')  # Explicitly using PBKDF2
            )
            db.session.add(admin)  # Add the admin user to the session
            db.session.commit()  # Commit the transaction to save the new admin
            print("Admin user created!")
        else:
            print("Admin user already exists!")


# Run the script to seed the admin user
if __name__ == "__main__":
    seed_admin()