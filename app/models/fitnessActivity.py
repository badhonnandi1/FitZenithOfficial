from app import db
from datetime import datetime

class FitnessActivity(db.Model):
    __tablename__ = 'fitness_activity'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    activity_type = db.Column(db.String(100), nullable=False)
    sub_type = db.Column(db.String(100), nullable=True)
    duration = db.Column(db.Integer, nullable=True)
    workout_volume = db.Column(db.Integer, nullable=False)
    reward_score = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @staticmethod
    def calculate_score_and_volume(activity_type, sub_type=None, duration=None):
        score = 0
        volume = 1  

        if activity_type == 'Weight Training':
            score = 20
        elif activity_type == 'Double Muscle Training (6 days)':
            score = 25
        elif activity_type == 'Single Muscle Training (6 days)':
            score = 15
        elif activity_type == 'Strength Training':
            score = 30
        elif activity_type in ['Cardio', 'Yoga']:
            if duration:
                score = duration * 1  
                volume = duration
            else:
                score = 5 
                
        return score, volume

    @staticmethod
    def add_activity(user_id, activity_type, sub_type=None, duration=None):
        from app.models.user import User

        reward_score, workout_volume = FitnessActivity.calculate_score_and_volume(
            activity_type, sub_type, duration
        )

        new_activity = FitnessActivity(
            user_id=user_id,
            activity_type=activity_type,
            sub_type=sub_type,
            duration=duration,
            workout_volume=workout_volume,
            reward_score=reward_score
        )
        db.session.add(new_activity)

        user = User.query.get(user_id)
        if user:
            user.total_workout_volume += workout_volume
            user.total_reward_score += reward_score
        
        db.session.commit()
        return new_activity

    @staticmethod
    def get_log_for_user(user_id):
        return FitnessActivity.query.filter_by(user_id=user_id).order_by(FitnessActivity.created_at.desc()).all()