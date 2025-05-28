from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

# creates -User model for user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(80), nullable=False)
    # email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # relationship for User and his Task
    tasks = db.relationship('Task', backref='owner', lazy=True)
    
    # hash the password
    def set_password(self, raw_password):
        self.password = generate_password_hash(raw_password)
        
    # check the hashed password
    def check_password(self, raw_password):
        return check_password_hash(self.password, raw_password)                   
    
# creates -Task model for the user
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    done = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))
    