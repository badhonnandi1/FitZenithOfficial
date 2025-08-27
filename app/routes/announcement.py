from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.announcement import Announcement, UserAnnouncementSeen
from app.models.user import User

announcement_bp = Blueprint('announcement', __name__)

@announcement_bp.route('/announcement/list')
def list_announcements():
    announcements = Announcement.get_all()
    if 'user_id' in session:
        # Mark all visible announcements as seen
        for announcement in announcements:
            UserAnnouncementSeen.mark_as_seen(session['user_id'], announcement.id)
            
    return render_template('announcements.html', announcements=announcements)

@announcement_bp.route('/announcement/create', methods=['GET', 'POST'])
def create_announcement():
    if session.get('role') not in ['admin', 'instructor']:
        flash('You do not have permission to create announcements.', 'error')
        return redirect(url_for('announcement.list_announcements'))

    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        Announcement.create(title, message, session['user_id'])
        flash('Announcement created successfully!', 'success')
        return redirect(url_for('announcement.list_announcements'))

    return render_template('create_announcement.html')

@announcement_bp.route('/announcement/update/<int:announcement_id>', methods=['GET', 'POST'])
def update_announcement(announcement_id):
    announcement = Announcement.get_by_id(announcement_id)
    if not announcement or (session.get('role') not in ['admin', 'instructor'] or announcement.author_id != session['user_id']):
        flash('You do not have permission to edit this announcement.', 'error')
        return redirect(url_for('announcement.list_announcements'))
    
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        announcement.update(title, message)
        flash('Announcement updated successfully!', 'success')
        return redirect(url_for('announcement.list_announcements'))

    return render_template('create_announcement.html', announcement=announcement)

@announcement_bp.route('/announcement/delete/<int:announcement_id>', methods=['POST'])
def delete_announcement(announcement_id):
    announcement = Announcement.get_by_id(announcement_id)
    if not announcement or (session.get('role') not in ['admin', 'instructor'] or announcement.author_id != session['user_id']):
        flash('You do not have permission to delete this announcement.', 'error')
        return redirect(url_for('announcement.list_announcements'))
    
    Announcement.delete(announcement_id)
    flash('Announcement deleted successfully.', 'success')
    return redirect(url_for('announcement.list_announcements'))