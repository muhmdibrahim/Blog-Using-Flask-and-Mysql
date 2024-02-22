from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://hemaa_ai:hemaa1234@localhost/login_user'

db = SQLAlchemy(app)

class accounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    status = db.Column(db.String(150))
    Posts = db.relationship('post', backref='accounts', passive_deletes=True)
    comments = db.relationship('comments', backref='accounts', passive_deletes=True)
    likes = db.relationship('likes', backref='accounts', passive_deletes=True)

class post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        'accounts.id', ondelete="CASCADE"), nullable=False)
    comments = db.relationship('comments', backref='post', passive_deletes=True)
    likes = db.relationship('likes', backref='post', passive_deletes=True)


class comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    author = db.Column(db.Integer, db.ForeignKey(
        'accounts.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)


class likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey(
        'accounts.id', ondelete="CASCADE"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey(
        'post.id', ondelete="CASCADE"), nullable=False)

'''
with app.app_context():
    # Fetch all users from the User table
    users = accounts.query.all()

    # Process the query results
    for user in users:
        print(user.id, user.email, user.username,user.Posts)

    posts = post.query.filter_by(author = 1)

    for post in posts:
        print(post.text)
'''