from app import db
from datetime import datetime
from sqlalchemy import text
from app.models.user import User

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref='posts', lazy=True)
    comments = db.relationship('Comment', backref='post', lazy=True, cascade="all, delete-orphan")

    @staticmethod
    def get_all():
        return Post.query.order_by(Post.created_at.desc()).all()

    @staticmethod
    def get_by_id(post_id):
        return Post.query.get_or_404(post_id)

    @staticmethod
    def create(title, content, user_id):
        new_post = Post(title=title, content=content, user_id=user_id, created_at=datetime.now())
        db.session.add(new_post)
        db.session.commit()
        return new_post

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    user = db.relationship('User', backref='comments', lazy=True)

    @staticmethod
    def create(content, user_id, post_id):
        time = datetime.now()
        new_comment = Comment(content=content, user_id=user_id, post_id=post_id, created_at=time)
        db.session.add(new_comment)
        db.session.commit()
        return new_comment