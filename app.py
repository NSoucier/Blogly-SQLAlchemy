# """Blogly application."""
# adapted to match JesseB's structure since I needed to create another instance of the app for testing (description saved in slack DMs)

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post
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


if __name__ == 'app':
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
#         asc_users = User.query.order_by(User.id).all()
#         return render_template('users.html', users=asc_users)
    
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