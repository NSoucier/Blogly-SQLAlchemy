
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag

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
        """ Show 5 most recent posts """
        posts = Post.query.order_by(Post.id.desc()).limit(5).all()
        return render_template('all_posts.html', posts=posts)
    
    @app.errorhandler(404)
    def page_not_found(e):
        """ Show error 404 page """

        return render_template('404.html'), 404

    ################ Section for handling users ################

    @app.route('/users')
    def show_users():
        """ Show all users """
        users = User.query.all()
        asc_users = User.query.order_by(User.id).all()

        return render_template('all_users.html', users=asc_users)
    
    @app.route('/users/new')
    def new_user_form():
        """ Show form to add new user """
        return render_template('new_user.html')

    @app.route('/users/new', methods=['POST'])
    def add_new_user():
        """ Process new user form """
        first = request.form['first']
        last = request.form['last']
        url = request.form['url'] or None
        
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
        posts = Post.query.filter_by(user_id=user_id).all()
        for post in posts:
            PostTag.query.filter_by(post_id=post.id).delete()

        Post.query.filter_by(user_id=user_id).delete() # delete users posts and commit first (couldn't get cascade working)
        db.session.commit()

        User.query.filter_by(id=user_id).delete()
        db.session.commit()
        return redirect('/users')
    
    ################ Section handling posts ################
    
    @app.route('/users/<int:user_id>/posts/new')
    def new_post_form(user_id):
        """ Show form to add post for that user """
        user = User.query.get_or_404(user_id)
        name = user.get_full_name()
        tags = Tag.query.order_by(Tag.id).all()

        return render_template('new_post.html', id=user_id, name=name, tags=tags)
    
    @app.route('/users/<int:user_id>/posts/new', methods=['POST'])
    def create_new_post(user_id):
        """ Create new post """
        title = request.form['title']
        content = request.form['content']
        post = Post(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        
        for key in request.form: # checks if any tags were added to the post
            if Tag.query.filter_by(name=key).all():
                postTag = PostTag(post_id=post.id, tag_id=Tag.query.filter_by(name=key).first().id)
                db.session.add(postTag)
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
        tags = Tag.query.order_by(Tag.id).all()
        
        return render_template('edit_post.html', post=post, tags=tags)

    @app.route('/posts/<int:post_id>/edit', methods=['POST'])
    def edit_post(post_id):
        """ Handle edit post form """
        post = Post.query.get_or_404(post_id)
        post.title = request.form['title']
        post.content = request.form['content']
        
        PostTag.query.filter_by(post_id=post_id).delete()
        for key in request.form: # checks if any tags were added to the post
            if Tag.query.filter_by(name=key).all():
                postTag = PostTag(post_id=post_id, tag_id=Tag.query.filter_by(name=key).first().id)
                db.session.add(postTag)
        
        db.session.add(post)
        db.session.commit()
        
        return redirect(f'/posts/{post_id}') 
    
    @app.route('/posts/<int:post_id>/delete', methods=['POST'])
    def delete_post(post_id):
        """ Deletes post """
        post = Post.query.get_or_404(post_id)
        user_id = post.user.id
        PostTag.query.filter_by(post_id=post_id).delete()
        Post.query.filter_by(id=post_id).delete()
        db.session.commit()
        return redirect(f'/users/{user_id}') 

    ################ Section for handling tags ################
    
    @app.route('/tags')
    def show_all_tags():
        """ List all tags """
        tags = Tag.query.order_by(Tag.id).all()
        return render_template('all_tags.html', tags=tags)
    
    @app.route('/tags/<int:tag_id>')
    def show_tag_posts(tag_id):
        """ Shows tag with related posts """
        tag = Tag.query.get_or_404(tag_id)
        return render_template('tag.html', tag=tag)
    
    @app.route('/tags/new')
    def new_tag_form():
        """ Shows form to add a new tag """
        return render_template('new_tag.html')
    
    @app.route('/tags/new', methods=['POST'])
    def create_tag():
        """ Handles new tag form """
        tag = Tag(name=request.form['tagname'])
        db.session.add(tag)
        db.session.commit()
        return redirect('/tags')
    
    @app.route('/tags/<int:tag_id>/edit')
    def edit_tag_form(tag_id):
        """ Shows form to edit tag """
        tag = Tag.query.get_or_404(tag_id)
        return render_template('edit_tag.html', tag=tag)
    
    @app.route('/tags/<int:tag_id>/edit', methods=['POST'])
    def edit_tag(tag_id):
        """ Handles edit tag form submission """
        tag = Tag.query.get_or_404(tag_id)
        tag.name = request.form['tagname']
        db.session.add(tag)
        db.session.commit()
        return redirect(f'/tags/{tag_id}')
    
    @app.route('/tags/<int:tag_id>/delete', methods=['POST'])
    def delete_tag(tag_id):
        """ Deletes tag """
        PostTag.query.filter_by(tag_id=tag_id).delete() # delete post-tag relationship first to avoid integrity error
        db.session.commit()
        Tag.query.filter_by(id=tag_id).delete()
        db.session.commit()
        
        return redirect('/tags')   

    return app


app = create_app(database_name='blogly', testing= False) # Here we are creating an instance of "app"
connect_db(app) # We call "connect_db(app)" here
