"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""
    
    with app.app_context():
        db.app = app
        db.init_app(app)
        db.create_all()

class User(db.Model):
    """User class"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, 
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(15),
                           nullable=False)
    last_name = db.Column(db.String(15),
                           nullable=False,
                           unique=True)    
    image_url = db.Column(db.String,
                          nullable=True,
                          default='https://cdn-icons-png.flaticon.com/512/1053/1053244.png')
    
    def __repr__(self):
        """ Show user id, first and last name """
        return f'id:{self.id} first:{self.first_name} last:{self.last_name}'
    
    def get_full_name(self):
        """ Return string of first and last name combined """
        return self.first_name + ' ' + self.last_name
    
# user1 = User(first_name='Jack', last_name='Johnson')
# db.session.add(user1)
# db.session.commit()