from app.db.database import SessionLocal
from app.models.user import User
from app.core.security import hash_password

def create_user():
    db = SessionLocal()

    user = User(
        email="admin@test.com",
        password=hash_password("admin123"),
        role="admin"
    )

    db.add(user)
    db.commit()
    db.close()

    print("User created successfully")

if __name__ == "__main__":
    create_user()