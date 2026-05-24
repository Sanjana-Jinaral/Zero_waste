from app import create_app
from models.user import User

app = create_app()
with app.app_context():
    users = User.query.all()
    print(f"Total users: {len(users)}")
    for user in users:
        print(f"Username: {user.username}, Email: {user.email}, Role: {user.role}")
