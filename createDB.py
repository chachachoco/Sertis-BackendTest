from app import db
from app.models import User, Card

db.create_all()

print("Database created.")