from unittest import TestCase
from app import create_app
from models import db, User, connect_db

class BloglyTests(TestCase):
    """ Tests for Blogly app """
    @classmethod
    def setUpClass(cls):
        """ Set up testing environment """
        cls.app = create_app("blogly_test", testing=True)
        cls.client = cls.app.test_client()

    # Establish application context
    with cls.app.app_context():
        # Initialize SQLAlchemy with the Flask application instance
        db.init_app(cls.app)
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        """ Clean up testing environment """
        # Drop all tables from the test database
        with cls.app.app_context():
            db.drop_all()

    def setUp(self):
        """ Add sample user before every test method """
        with self.app.app_context():
            # Create a new database session for each test
            self.db = db.session
            user = User(first_name='test', last_name='1', image_url='https://upload.wikimedia.org/wikipedia/commons/b/bd/Test.svg')
            self.db.add(user)
            self.db.commit()

            self.user_id = user.id

    def tearDown(self):
        """ Clean up any fouled transaction after every test method """
        # Rollback the current transaction to clean up the database state
        # self.db.rollback()
        with self.app.app_context():
            User.query.delete()
            self.db.commit()

    def test_show_users(self):
        """ Check to see if user is displayed in list """
        resp = self.client.get("/users")
        html = resp.get_data(as_text=True)
        print(html, "*************************")
        self.assertEqual(resp.status_code, 200)
        # self.assertIn('Firstname Lastname', html)
        
    def test_show_user_details(self):
        """ Check to see if user details is displayed """
        resp = self.client.get(f"/users/{self.user_id}")
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        # self.assertIn('Firstname Lastname', html)

    def test_show_edit_user(self):
        """ Check to see if user is populated on 'edit user' page """
        resp = self.client.get(f"/users/{self.user_id}/edit")
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        # self.assertIn('Firstname', html)

    def test_delete_user(self):
        """ Check to see if user is deleted from db """
        post = self.client.post(f"/users/{self.user_id}/delete")
        resp = self.client.get('/users')
        html = resp.get_data(as_text=True)
        self.assertEqual(resp.status_code, 200)
        # self.assertNotIn('Firstname', html)

#############################################################################################
# """Blogly application."""
# adapted to match JesseB's structure since I needed to create another instance of the app for testing (description saved in slack DMs)

from flask import Flask, request, redirect, render_template
from .models import db, connect_db, User

from flask_debugtoolbar import DebugToolbarExtension

def create_app(database_name, testing=False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{database_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SECRET_KEY'] = "secret"
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    if testing:
    app.config["WTF_CSRF_ENABLED"] = False

    debug = DebugToolbarExtension(app)
    @app.route('/')
    def show_home():
        """ Redirect to list of users """
        return redirect('/users')
    
    @app.route('/users')
    def show_users():
        """ Show all users """
        users = User.query.all()
        asc_users = User.query.order_by(User.id).all()

        return render_template('users.html', users=asc_users)
    
    @app.route('/users/new')
    def new_user_form():
        """ Show form to add new user """
        return render_template('new_user.html')

    @app.route('/users/new', methods=['POST'])
    def add_new_user():
        """ Process new user form """
        first = request.form['first']
        last = request.form['last']
        url = request.form['url']
        user = User(first_name=first, last_name=last, image_url=url)
        db.session.add(user)
        db.session.commit()
        return redirect('/users')

    @app.route('/users/<int:user_id>')
    def show_user(user_id):
        """ Show information about specific user """
        user = User.query.get_or_404(user_id)
        return render_template('user_details.html', id=user_id, user=user)

    @app.route('/users/<int:user_id>/edit')
    def edit_user_form(user_id):
        """ Show edit page for a user """
        user = User.query.get_or_404(user_id)
        return render_template('edit_user.html', id=user_id, user=user)

    @app.route('/users/<int:user_id>/edit', methods=['POST'])
    def edits_user(user_id):
        """ Process edit form """
        user = User.query.get_or_404(user_id)
        user.first_name = request.form['first']
        user.last_name = request.form['last']
        user.image_url = request.form['url']
        db.session.add(user)
        db.session.commit()
        return redirect('/users')

    @app.route('/users/<int:user_id>/delete', methods=['POST'])
    def delete_user(user_id):
        """ Deletes user """
        User.query.filter_by(id=user_id).delete()
        db.session.commit()
        return redirect('/users')
    
    @app.route('/users/<int:user_id>/posts/new')
    def new_post_form(user_id):
        """ Show form to add post for that user """
        user = User.query.get_or_404(user_id)
        name = user.get_full_name()

        return render_template('new_post.html', id=user_id, name=name)
    
    @app.route('/users/<int:user_id>/posts/new', methods=['POST'])
    def create_new_post(user_id):
        """ Create new post """
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(f'/users/{user_id}')
    
    @app.route('/posts/<int:post_id>')
    def show_post(post_id):
        """ Show a post """
        post = Post.query.get_or_404(post_id)

        return render_template('post_details.html', post=post)
    
    @app.route('/posts/<int:post_id>/edit')
    def edit_post_form(post_id):
        """ Show form to edit a post """
        post = Post.query.get_or_404(post_id)
        return render_template('edit_post.html', post=post)

    @app.route('/posts/<int:post_id>/edit', methods=['POST'])
    def edit_post(post_id):
        """ Handle edit post form """
        post = Post.query.get_or_404(post_id)
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.add(post)
        db.session.commit()
        return redirect(f'/posts/{post_id}') 
    
    @app.route('/posts/<int:post_id>/delete', methods=['POST'])
    def delete_post(post_id):
        """ Deletes post """
        post = Post.query.get_or_404(post_id)
        user_id = post.user.id
        Post.query.filter_by(id=post_id).delete()
        db.session.commit()
        return redirect(f'/users/{user_id}') 

    return app


# if __name__ == '__main__':
app = create_app(database_name='blogly', testing= False) # Here we are creating an instance of "app"
connect_db(app) # We call "connect_db(app)" here
# app.run(debug=True)

###########################