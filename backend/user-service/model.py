from flask_sqlalchemy import SQLAlchemy
import hashlib

db = SQLAlchemy()


# UNSAFE!!
def hash_password(password) -> str:
    return hashlib.md5(password.encode()).hexdigest()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __repr__(self) -> str:
        return "<User %r>" % self.username

    def check_password(self, password) -> bool:
        return hash_password(password) == self.password_hash

    def set_password(self, new_password):
        self.password_hash = hash_password(new_password)

    def as_dict(self):
        return {"id": self.id, "username": self.username, "email": self.email}
