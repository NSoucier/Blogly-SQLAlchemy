# """Blogly application."""
# adapted to match JesseB's structure since I needed to create another instance of the app for testing (description saved in slack DMs)

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
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
        # show in order
        # asc_users = sorted(users)
        return render_template('users.html', users=users)
    
    @app.route('/users/new')
    def new_user_form():
        """ Show form to add new user """
        return render_template('new_user.html')
    
    return app


if __name__ == '__main__':
    print('((((((((((((((()))))))))))))))')
    app = create_app('blogly')   # Here we are creating an instance of "app"
    connect_db(app)                # We call "connect_db(app)" here
    app.run(debug=True)

###########################

# def create_app(database_name, testing=False):
#     from flask import Flask, request, redirect, render_template
#     from models import db, connect_db, User
#     from flask_debugtoolbar import DebugToolbarExtension

#     app = Flask(__name__)
#     app.config['SECRET_KEY'] = "SECRET!"
#     app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql:///{database_name}'
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SQLALCHEMY_ECHO'] = True
#     if testing:
#         app.config["WTF_CSRF_ENABLED"] = False
        
#     debug = DebugToolbarExtension(app)

#     connect_db(app)
#     # db.create_all() # This makes flask run fail for some reason
        
#     @app.route('/')
#     def show_home():
#         """ Redirect to list of users """
#         return redirect('/users')
    
#     @app.route('/users')
#     def show_users():
#         """ Show all users """
#         users = User.query.all()
#         # show in order
#         # asc_users = sorted(users)
#         return render_template('users.html', users=users)
    
#     @app.route('/users/new')
#     def new_user_form():
#         """ Show form to add new user """
#         return render_template('new_user.html')

#     @app.route('/users/new', methods=['POST'])
#     def add_new_user():
#         """ Process new user form """
#         first = request.form['first']
#         last = request.form['last']
#         url = request.form['url']
        
#         user = User(first_name=first, last_name=last, image_url=url)
#         db.session.add(user)
#         db.session.commit()
        
#         return redirect('/users')

#     @app.route('/users/<int:user_id>')
#     def show_user(user_id):
#         """ Show information about specific user """
#         user = User.query.get(user_id)
#         return render_template('user_details.html', id=user_id, user=user)

#     @app.route('/users/<int:user_id>/edit')
#     def edit_user_form(user_id):
#         """ Show edit page for a user """
#         user = User.query.get(user_id)
#         return render_template('edit_user.html', id=user_id, user=user)

#     @app.route('/users/<int:user_id>/edit', methods=['POST'])
#     def edits_user(user_id):
#         """ Process edit form """
#         user = User.query.get(user_id)
#         user.first_name = request.form['first']
#         user.last_name = request.form['last']
#         user.image_url = request.form['url']
        
#         db.session.add(user)
#         db.session.commit()
#         return redirect('/users')

#     @app.route('/users/<int:user_id>/delete', methods=['POST'])
#     def delete_user(user_id):
#         """ Deletes user """
#         User.query.filter_by(id=user_id).delete()
#         db.session.commit()
#         return redirect('/users')

#     return app

# from models import connect_db
# print('((((((((((((((((((()))))))))))))))))))', __name__)

# if __name__ == '__main__':
#     print('((((((((((((((((((()))))))))))))))))))')
#     app = create_app('blogly')   # Here we are creating an instance of "app"
#     connect_db(app)                # We call "connect_db(app)" here
#     app.run(debug=True)

# # You can now run this via "python3 -m app" in the command line

# -----------------------------------------------------------------------------
# old method below

# """Blogly application."""

# from flask import Flask, request, redirect, render_template
# from flask import session
# from models import db, connect_db, User
# from flask_debugtoolbar import DebugToolbarExtension

# app = Flask(__name__)
# app.config['SECRET_KEY'] = "SECRET!"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ECHO'] = True
# debug = DebugToolbarExtension(app)

# connect_db(app)
# app.app_context()
# # db.create_all() # This makes flask run fail for some reason
    
# @app.route('/')
# def show_home():
#     """ Redirect to list of users """
#     return redirect('/users')
 
# @app.route('/users')
# def show_users():
#     """ Show all users """
#     users = User.query.all()
#     asc_users = User.query.order_by(User.id).all()

#     return render_template('users.html', users=asc_users)
 
# @app.route('/users/new')
# def new_user_form():
#     """ Show form to add new user """
#     return render_template('new_user.html')

# @app.route('/users/new', methods=['POST'])
# def add_new_user():
#     """ Process new user form """
#     first = request.form['first']
#     last = request.form['last']
#     url = request.form['url']
    
#     user = User(first_name=first, last_name=last, image_url=url)
#     db.session.add(user)
#     db.session.commit()
    
#     return redirect('/users')

# @app.route('/users/<int:user_id>')
# def show_user(user_id):
#     """ Show information about specific user """
#     user = User.query.get(user_id)
#     return render_template('user_details.html', id=user_id, user=user)

# @app.route('/users/<int:user_id>/edit')
# def edit_user_form(user_id):
#     """ Show edit page for a user """
#     user = User.query.get(user_id)
#     return render_template('edit_user.html', id=user_id, user=user)

# @app.route('/users/<int:user_id>/edit', methods=['POST'])
# def edits_user(user_id):
#     """ Process edit form """
#     user = User.query.get(user_id)
#     user.first_name = request.form['first']
#     user.last_name = request.form['last']
#     user.image_url = request.form['url']
    
#     db.session.add(user)
#     db.session.commit()
#     return redirect('/users')

# @app.route('/users/<int:user_id>/delete', methods=['POST'])
# def delete_user(user_id):
#     """ Deletes user """
#     User.query.filter_by(id=user_id).delete()
#     db.session.commit()
#     return redirect('/users')