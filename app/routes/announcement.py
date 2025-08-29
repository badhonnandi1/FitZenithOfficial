from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.announcement import Announcement, UserAnnouncementSeen
from app.models.user import User

announcement_bp = Blueprint('announcement', __name__)

@announcement_bp.route('/announcement/list')
def list_announcements():
    announcements = Announcement.allAnnouncement() 
    if 'user_id' in session:
        for x in announcements:
            UserAnnouncementSeen.seenMessage(session['user_id'], x.id)
            
    return render_template('announcements.html', announcements=announcements)

@announcement_bp.route('/announcement/create', methods=['GET', 'POST'])
def createAnnouncement():
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        Announcement.create(title, message, session['user_id'])

        flash('Announcement created successfully!', 'success')
        return redirect('/announcement/list')

    return render_template('createAnnouncement.html')

@announcement_bp.route('/announcement/update/<id>', methods=['GET', 'POST'])
def updateAnnouncement(id):
    announcement = Announcement.getByID(id)    
    if request.method == 'POST':
        title = request.form['title']
        message = request.form['message']
        announcement.update(title, message)
        flash('Updated', 'success')
        return redirect('/announcement/list')

    return render_template('createAnnouncement.html', announcement=announcement)

@announcement_bp.route('/announcement/delete/<id>', methods=['POST'])
def delete_announcement(id):
    announcement = Announcement.getByID(id)
    if not announcement or (session.get('role') not in ['admin', 'instructor'] or announcement.author_id != session['user_id']):
        return redirect('/announcement/list')
    
    Announcement.delete(id)
    flash('Deleted', 'success')
    return redirect('/announcement/list')