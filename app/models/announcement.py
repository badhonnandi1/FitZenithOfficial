from app import db
from datetime import datetime

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    author = db.relationship('User', backref='announcements', lazy=True)
    seen_by = db.relationship('UserAnnouncementSeen', backref='announcement', lazy=True, cascade="all, delete-orphan")

    @staticmethod
    def get_all():
        return Announcement.query.order_by(Announcement.date_created.desc()).all()

    @staticmethod
    def get_by_id(announcement_id):
        return Announcement.query.get(announcement_id)

    @staticmethod
    def create(title, message, author_id):
        new_announcement = Announcement(title=title, message=message, author_id=author_id)
        db.session.add(new_announcement)
        db.session.commit()
        return new_announcement

    def update(self, title, message):
        self.title = title
        self.message = message
        db.session.commit()

    @staticmethod
    def delete(announcement_id):
        announcement = Announcement.get_by_id(announcement_id)
        if announcement:
            db.session.delete(announcement)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_latest_unseen_announcement(user_id):
        latest_announcement = Announcement.query.order_by(Announcement.date_created.desc()).first()
        if not latest_announcement:
            return None

        seen = UserAnnouncementSeen.query.filter_by(user_id=user_id, announcement_id=latest_announcement.id).first()
        if seen:
            return None
        
        return latest_announcement

class UserAnnouncementSeen(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    announcement_id = db.Column(db.Integer, db.ForeignKey('announcement.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def mark_as_seen(user_id, announcement_id):
        if not UserAnnouncementSeen.query.filter_by(user_id=user_id, announcement_id=announcement_id).first():
            seen = UserAnnouncementSeen(user_id=user_id, announcement_id=announcement_id)
            db.session.add(seen)
            db.session.commit()