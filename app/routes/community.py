from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models.community import Post, Comment
from app.models.user import User

community_bp = Blueprint('community', __name__)

@community_bp.route('/community')
def list_posts():
    all_posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('listPost.html', posts=all_posts)

@community_bp.route('/community/post/<int:post_id>')
def post_details(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('postDetails.html', post=post) 

@community_bp.route('/community/createpost', methods=['GET'])
def create_post_form():
    if 'user_id' not in session:
        flash('You must be logged in to create a post.', 'error')
        return redirect('/login')
    
    return render_template('createPost.html')

@community_bp.route('/community/postcreate', methods=['POST'])
def create_post():
    if 'user_id' not in session:
        flash('You must be logged in to create a post.', 'error')
        return redirect('/login')
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = session.get('user_id')

        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('community.list_posts'))
        
    return render_template('createPost.html')

@community_bp.route('/community/post/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if 'user_id' not in session:
        flash('You must be logged in to comment.', 'error')
        return redirect('/login')
    
    post = Post.query.get_or_404(post_id)
    content = request.form.get('content')
    user_id = session.get('user_id')

    if not content:
        flash('Comment cannot be empty.', 'error')
        return redirect(url_for('community.post_details', post_id=post.id))

    new_comment = Comment(content=content, user_id=user_id, post_id=post.id)
    db.session.add(new_comment)
    db.session.commit()
    flash('Comment added successfully!', 'success')
    return redirect(url_for('community.post_details', post_id=post_id))