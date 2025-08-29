from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.community import Post, Comment
from app.models.user import User

community_bp = Blueprint('community', __name__)

@community_bp.route('/community')
def list_posts():
    all_posts = Post.get_all()
    return render_template('listPost.html', posts=all_posts)

@community_bp.route('/community/post/<post_id>')
def post_details(post_id):
    post = Post.get_by_id(post_id)
    return render_template('postDetails.html', post=post) 

@community_bp.route('/community/createpost', methods=['GET'])
def create_post_form():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    return render_template('createPost.html')

@community_bp.route('/community/postcreate', methods=['POST'])
def create_post():    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = session.get('user_id')

        Post.create(title, content, user_id)
        
        flash('Post created successfully!', 'success')
        return redirect('/community')
        
    return render_template('createPost.html')

@community_bp.route('/community/post/<post_id>/comment', methods=['POST'])
def add_comment(post_id):
    if 'user_id' not in session:
        flash('You must be logged in to comment.', 'error')
        return redirect(url_for('auth.login'))
    
    content = request.form.get('content')
    user_id = session.get('user_id')

    if not content:
        flash('Comment cannot be empty.', 'error')
        return redirect(url_for('community.post_details', post_id=post_id))

    Comment.create(content, user_id, post_id)
    
    flash('Comment added successfully!', 'success')
    return redirect(f'/community/post/{post_id}')
