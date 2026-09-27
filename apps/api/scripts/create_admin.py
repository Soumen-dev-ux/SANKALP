from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models.user import User


db = SessionLocal()

try:
    email = "admin@sankalp.local"

    existing = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing:
        existing.role = "admin"
        existing.is_active = True
        db.commit()
        print("Existing user promoted to admin.")
    else:
        admin = User(
            email=email,
            password_hash=hash_password(
                "SankalpAdmin123!"
            ),
            full_name="SANKALP Administrator",
            role="admin",
            is_active=True,
        )

        db.add(admin)
        db.commit()

        print("Admin user created.")

finally:
    db.close()