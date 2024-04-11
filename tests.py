from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_tests'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# db.drop_all()
# db.create_all()
print('((((((((((((((((((((((()))))))))))))))))))))))')

class BloglyTests(TestCase):
    """ Tests for Blogly app """
    
    def setUp(self):
        """ Add sample user before every test method """

        User.query.delete()

        user = User(first_name='Firstname', last_name='Lastname', image_url='https://upload.wikimedia.org/wikipedia/commons/b/bd/Test.svg')
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """ Clean up any fouled transaction after every test method """

        db.session.rollback()
    
    def show_users_test(self):
        """ Check to see if user is displayed in list """
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Firstname Lastname', html)
    
    def show_user_details_test(self):
        """ Check to see if user details is displayed """
        with app.test_client() as client:
            resp = client.get("/users/1")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Firstname Lastname', html)

    def show_edit_user_test(self):
        """ Check to see if user is populated on 'edit user' page """
        with app.test_client() as client:
            resp = client.get("/users/1/edit")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Firstname', html)

    def delete_user_test(self):
        """ Check to see if user is deleted from db """
        with app.test_client() as client:
            post = client.post("/users/1/delete")
            resp = client.get('/users')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Firstname', html)