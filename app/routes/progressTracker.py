from flask import Blueprint, render_template, request, redirect, session, flash
from app.models.fitnessActivity import FitnessActivity
from app.models.user import User

progress_tracker_bp = Blueprint('progress_tracker', __name__)

mydict = {
    'Weight Training': {
        'sub_options': ['Back & Biceps Day', 'Chest & Shoulder Day', 'Leg & Abs Day']
    },
    'Double Muscle Training (6 days)': {},
    'Single Muscle Training (6 days)': {},
    'Cardio': {
        'requires_duration': True
    },
    'Yoga': {
        'requires_duration': True
    },
    'Football': {
        'requires_duration': True
    },
    'Strength Training': {
        'sub_options': ['Deadlift', 'Squats','Bench Press']
    }
}

@progress_tracker_bp.route('/progress-tracker', methods=['GET', 'POST'])
def tracker_page():

    user_id = session['user_id']

    if request.method == 'POST':
        activity_type = request.form.get('activity_type')
        sub_type = request.form.get('sub_type')
        duration_str = request.form.get('duration')
        
        duration = int(duration_str) if duration_str else None

        if activity_type in mydict:
            FitnessActivity.add_activity(user_id, activity_type, sub_type, duration)
            flash(f'Successfully logged "{activity_type}" activity!', 'success')
        else:
            flash('Invalid activity selected.', 'error')
        
        return redirect('/progress-tracker')

    user = User.getUser(user_id)
    activity_log = FitnessActivity.get_log_for_user(user_id)
    
    return render_template(
        'progress_tracker.html', 
        activities_config=mydict, 
        activity_log=activity_log,
        user=user
    )

@progress_tracker_bp.route('/leaderboard')
def leaderboard():
    users = User.leaderboardlist()
    return render_template('leaderboard.html', users=users)