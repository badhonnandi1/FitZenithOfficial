from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.foodTracking import Food, FoodLog
from datetime import date

food_tracking_bp = Blueprint('food_tracking', __name__)

@food_tracking_bp.route('/food-tracking', methods=['GET'])
def food_tracking_page():
    current_date = date.today()
    user_id = session['user_id']
    
    foodSearched = request.args.get('query', '') #mamural search korte parbo ami eita diye

    if foodSearched:
        available_foods = Food.search(foodSearched)
    else:
        available_foods = Food.get_all()
    
    food_logs = FoodLog.get_log_by_date(user_id, current_date)
    
    total_calories, total_fat, total_protein = FoodLog.get_total_nutrients(user_id, current_date)
    
    return render_template('foodTracking.html', all_food_logs=food_logs, total_calories=total_calories, total_fat=total_fat, total_protein=total_protein, available_foods=available_foods, foodSearched=foodSearched)

@food_tracking_bp.route('/food-tracking/add', methods=['POST'])
def add_food_log():
    if 'user_id' not in session:
        flash('You must be logged in to track food.', 'error')
        return redirect('/login')
    
    user_id = session['user_id']
    food_id = request.form.get('food_id')
    meal_type = request.form.get('meal_type')

    FoodLog.create_log(user_id, food_id, meal_type, date.today())
    flash(f'Food item added to {meal_type}!', 'success')
    return redirect('/food-tracking')

@food_tracking_bp.route('/food-tracking/delete', methods=['POST'])
def delete_food_log():     
    log_id = request.form.get('log_id')
    food_log = FoodLog.query.get(log_id)
    
    FoodLog.delete_log(log_id)
    flash('Food item deleted successfully!', 'success')
    return redirect('/food-tracking')