from unittest import TestCase
from app import create_app
from models import db, User, Post, Tag, PostTag

class BloglyTests(TestCase):
    """ Tests for Blogly app """
    @classmethod
    def setUpClass(cls):
        """ Set up testing environment """
        cls.app = create_app("blogly_test", testing=True)
        cls.client = cls.app.test_client()
        # Don't clutter tests with SQL
        cls.app.config['SQLALCHEMY_ECHO'] = False 
        # Make Flask errors be real errors, rather than HTML pages with error info
        cls.app.config['TESTING'] = True      
        # This is a bit of hack, but don't use Flask DebugToolbar
        cls.app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

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
            db.create_all()
            # Create a new database session for each test
            self.db = db.session
            user = User(first_name='Firstname', last_name='Lastname', image_url='https://upload.wikimedia.org/wikipedia/commons/b/bd/Test.svg')
            self.db.add(user)
            self.db.commit()
            
            post = Post(title='Testing title', content='Testing content', user_id=user.id)
            self.db.add(post)
            self.db.commit()
            
            tag = Tag(name='Testing tag')
            self.db.add(tag)
            self.db.commit() 

            self.user_id = user.id
            self.post_id = post.id
            self.tag_id = tag.id

            posttag = PostTag(tag_id=self.tag_id, post_id=self.post_id)
            self.db.add(posttag)
            self.db.commit() 

    def tearDown(self):
        """ Clean up any fouled transaction after every test method """
        with self.app.app_context():
            PostTag.query.delete()
            Tag.query.delete()
            Post.query.delete()
            User.query.delete()
            self.db.commit()
            db.drop_all()

    ############## Tests for users section of app

    def test_show_users(self):
        """ Check to see if user is displayed in list """
        resp = self.client.get("/users")
        html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Firstname Lastname', html)
        
    def test_show_user_details(self):
        """ Check to see if user details is displayed """
        resp = self.client.get(f"/users/{self.user_id}")
        html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Firstname Lastname', html)

    def test_show_edit_user(self):
        """ Check to see if user is populated on 'edit user' page """
        resp = self.client.get(f"/users/{self.user_id}/edit")
        html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Firstname', html)

    def test_delete_user(self):
        """ Check to see if user is deleted from db """
        user = self.client.post(f"/users/{self.user_id}/delete")
        resp = self.client.get('/users')
        html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('Firstname', html)
    
    ############## Tests for posts section of app
    
    def test_show_post(self):
        """ Check to see if post is displayed on user page """
        resp = self.client.get(f"/users/{self.user_id}")
        html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Testing title', html)
    
    def test_show_post_details(self):
        """ Check to see if post content is displayed """
        resp = self.client.get(f"/posts/{self.post_id}")
        html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Testing content', html)

    def test_edit_post(self):
        """ Check to see if post details are populated on 'edit post' page """
        resp = self.client.get(f"/posts/{self.post_id}/edit")
        html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Testing title', html)

    def test_delete_post(self):
        """ Check to see if post is deleted from db """
        post = self.client.post(f"/posts/{self.post_id}/delete")
        resp = self.client.get(f'/users/{self.user_id}')
        html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('Testing title', html)
        
    ############# Tests for tags section of app
    
    def test_show_tag_list(self):
        """ Check to see if tag is displayed on all tags page """
        resp = self.client.get("/tags")
        html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Testing tag', html)
            
    def test_show_tag_details(self):
        """ Check to see if post content is displayed on the tag page """
        resp = self.client.get(f"/tags/{self.tag_id}")
        html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Testing title', html)
            
    def test_show_tag_on_post(self):
        """ Check to see if tag is displayed on post on the homepage """
        resp = self.client.get("/")
        html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Testing content', html)
        self.assertIn('Testing tag', html)

    def test_edit_tag(self):
        """ Check to see if tag name is populated on 'edit tag' page """
        resp = self.client.get(f"/tags/{self.tag_id}/edit")
        html = resp.get_data(as_text=True)
        
        self.assertEqual(resp.status_code, 200)
        self.assertIn('Testing tag', html)

