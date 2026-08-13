# app/models.py
from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager, bcrypt

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationship to cases (one user -> many cases)
    cases = db.relationship("Case", backref="owner", lazy=True)

    def set_password(self, password: str):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"

#Update case model to include client_address case_summary, and it has client_last_name
class Case(db.Model):
    __tablename__ = "cases"

    id = db.Column(db.Integer, primary_key=True)

    client_name = db.Column(db.String(120), nullable=False)
    raft_case_number = db.Column(db.String(64), nullable=False, index=True)
    client_address = db.Column(db.String(255))

    status = db.Column(db.String(80))
    case_summary = db.Column(db.Text)

    submitted_date = db.Column(db.String(80))
    last_checked_at = db.Column(db.DateTime)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    def __repr__(self):
        return f"<Case {self.raft_case_number} - {self.client_name}>"
