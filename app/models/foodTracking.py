from app import db
from sqlalchemy import text
from datetime import datetime, date

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)

    @staticmethod
    def get_all():
        return Food.query.all()
    
    @staticmethod
    def search(query):
        return Food.query.filter(Food.name.like(f'%{query}%')).all()

class FoodLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    meal_type = db.Column(db.String(20), nullable=False)  # 'Breakfast', 'Lunch', 'Dinner'
    log_date = db.Column(db.Date, nullable=False, default=date.today)

    food = db.relationship('Food', backref='food_logs', lazy=True)
    user = db.relationship('User', backref='food_logs', lazy=True)

    @staticmethod
    def get_log_by_date(user_id, log_date):
        return FoodLog.query.filter_by(user_id=user_id, log_date=log_date).all()
        
    @staticmethod
    def get_total_nutrients(user_id, log_date):
        logs = FoodLog.get_log_by_date(user_id, log_date)
        total_calories = sum(log.food.calories for log in logs)
        total_fat = sum(log.food.fat for log in logs)
        total_protein = sum(log.food.protein for log in logs)
        return total_calories, total_fat, total_protein

    @staticmethod
    def create_log(user_id, food_id, meal_type, log_date):
        new_log = FoodLog(
            user_id=user_id,
            food_id=food_id,
            meal_type=meal_type,
            log_date=log_date
        )
        db.session.add(new_log)
        db.session.commit()
        return new_log

    @staticmethod
    def delete_log(log_id):
        log = FoodLog.query.get(log_id)
        if log:
            db.session.delete(log)
            db.session.commit()