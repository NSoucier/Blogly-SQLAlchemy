"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """ Connect to database """
    
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()

class User(db.Model):
    """ User class """
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(15),
                           nullable=False)
    last_name = db.Column(db.String(15),
                           nullable=False)
    image_url = db.Column(db.Text,
                          nullable=False,
                          default="https://cdn-icons-png.flaticon.com/512/1053/1053244.png")
    
    posts = db.relationship("Post", backref="user") # tried adding this in, but still got integrity error (cascade="all, delete-orphan")
                            
    def __repr__(self):
        """ Show user id, first and last name """
        return f'<id:{self.id} first:{self.first_name} last:{self.last_name}>'
    
    def get_full_name(self):
        """ Return string of first and last name combined """
        return self.first_name + ' ' + self.last_name
    
class Post(db.Model):
    """ Post class """
    
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.now())
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    tags = db.relationship('Tag', secondary='posts_tags', backref='posts')
        
    def __repr__(self):
        """ Show user first name and post title"""
        return f'<Name:{self.user.first_name} title:{self.title}>'
    
class Tag(db.Model):
    """ Tag class """
    
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer,
                   primary_key=True, 
                   autoincrement=True)
    name = db.Column(db.Text,
                     unique=True,
                     nullable=False)
    
    def __repr__(self):
        """ Show name of tag """
        return f'<Tag:{self.name}>'
    
class PostTag(db.Model):
    """ Mapping of a post to a tag """
    
    __tablename__ = 'posts_tags'
    
    post_id = db.Column(db.Integer,
                        db.ForeignKey('posts.id'),
                        primary_key=True)
    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tags.id'),
                       primary_key=True)
    
    
    