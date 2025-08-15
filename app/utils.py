from app.models.foodTracking import Food
from app import db

def load_sample_food_data():
    sample_foods = [
        # Fruits
        {'name': 'Apple', 'calories': 95, 'fat': 0.3, 'protein': 0.5},
        {'name': 'Banana', 'calories': 105, 'fat': 0.4, 'protein': 1.3},
        {'name': 'Orange', 'calories': 62, 'fat': 0.2, 'protein': 1.2},
        {'name': 'Strawberries (1 cup)', 'calories': 49, 'fat': 0.5, 'protein': 1.0},
        {'name': 'Grapes (1 cup)', 'calories': 104, 'fat': 0.2, 'protein': 1.1},
        
        {'name': 'Broccoli (1 cup)', 'calories': 55, 'fat': 0.6, 'protein': 3.7},
        {'name': 'Spinach (1 cup)', 'calories': 7, 'fat': 0.1, 'protein': 0.9},
        {'name': 'Carrot (medium)', 'calories': 25, 'fat': 0.1, 'protein': 0.6},
        {'name': 'Sweet Potato (medium)', 'calories': 103, 'fat': 0.2, 'protein': 2.3},
        {'name': 'Avocado (half)', 'calories': 160, 'fat': 14.7, 'protein': 2.0},

        {'name': 'Oatmeal (1 cup cooked)', 'calories': 150, 'fat': 2.6, 'protein': 5.5},
        {'name': 'Brown Rice (1 cup cooked)', 'calories': 216, 'fat': 1.8, 'protein': 5.0},
        {'name': 'Whole Wheat Bread (1 slice)', 'calories': 82, 'fat': 1.1, 'protein': 4.0},
        {'name': 'Quinoa (1 cup cooked)', 'calories': 222, 'fat': 3.6, 'protein': 8.1},
        {'name': 'Pasta (1 cup cooked)', 'calories': 200, 'fat': 1.3, 'protein': 7.0},

        {'name': 'Chicken Breast (cooked, 100g)', 'calories': 165, 'fat': 3.6, 'protein': 31.0},
        {'name': 'Salmon (cooked, 100g)', 'calories': 208, 'fat': 13.0, 'protein': 20.0},
        {'name': 'Tofu (100g)', 'calories': 76, 'fat': 4.8, 'protein': 8.0},
        {'name': 'Eggs (1 large)', 'calories': 72, 'fat': 4.8, 'protein': 6.3},
        {'name': 'Lentils (1 cup cooked)', 'calories': 230, 'fat': 0.8, 'protein': 18.0},

        {'name': 'Greek Yogurt (1 cup)', 'calories': 130, 'fat': 0.8, 'protein': 20.0},
        {'name': 'Milk (1 cup, 2%)', 'calories': 122, 'fat': 4.8, 'protein': 8.1},
        {'name': 'Cheddar Cheese (1 slice)', 'calories': 113, 'fat': 9.3, 'protein': 7.0},
        {'name': 'Almond Milk (1 cup)', 'calories': 39, 'fat': 2.8, 'protein': 1.5},
        {'name': 'Cottage Cheese (1 cup)', 'calories': 163, 'fat': 2.3, 'protein': 28.0},
        # Fats & Oils
        {'name': 'Olive Oil (1 tbsp)', 'calories': 119, 'fat': 13.5, 'protein': 0.0},
        {'name': 'Almonds (1 oz)', 'calories': 164, 'fat': 14.2, 'protein': 6.0},
        {'name': 'Peanut Butter (2 tbsp)', 'calories': 190, 'fat': 16.0, 'protein': 7.0},
        {'name': 'Walnuts (1 oz)', 'calories': 185, 'fat': 18.5, 'protein': 4.3},
        {'name': 'Butter (1 tbsp)', 'calories': 102, 'fat': 11.5, 'protein': 0.1},
        # Meals & Snacks
        {'name': 'Chicken Salad Sandwich', 'calories': 350, 'fat': 15.0, 'protein': 25.0},
        {'name': 'Beef Burger', 'calories': 550, 'fat': 30.0, 'protein': 30.0},
        {'name': 'Pizza (1 slice)', 'calories': 285, 'fat': 10.0, 'protein': 12.0},
        {'name': 'Salad with Vinaigrette', 'calories': 200, 'fat': 15.0, 'protein': 5.0},
        {'name': 'Protein Shake', 'calories': 250, 'fat': 5.0, 'protein': 30.0},
        {'name': 'Smoothie', 'calories': 220, 'fat': 4.0, 'protein': 10.0},
        {'name': 'Energy Bar', 'calories': 180, 'fat': 8.0, 'protein': 10.0},
        {'name': 'Sushi (8 pieces)', 'calories': 300, 'fat': 5.0, 'protein': 15.0},
        {'name': 'Taco', 'calories': 250, 'fat': 12.0, 'protein': 10.0},
        {'name': 'Spaghetti Bolognese', 'calories': 600, 'fat': 25.0, 'protein': 35.0},
        {'name': 'Grilled Cheese Sandwich', 'calories': 400, 'fat': 20.0, 'protein': 15.0},
        # Desserts
        {'name': 'Ice Cream (1 scoop)', 'calories': 150, 'fat': 8.0, 'protein': 2.0},
        {'name': 'Chocolate Chip Cookie', 'calories': 160, 'fat': 8.0, 'protein': 2.0},
        {'name': 'Brownie', 'calories': 250, 'fat': 12.0, 'protein': 3.0},
        {'name': 'Fruit Salad', 'calories': 120, 'fat': 0.5, 'protein': 1.5},
        {'name': 'Cheesecake (1 slice)', 'calories': 320, 'fat': 20.0, 'protein': 7.0},
        # Drinks
        {'name': 'Coffee with milk', 'calories': 30, 'fat': 1.5, 'protein': 1.5},
        {'name': 'Green Tea', 'calories': 0, 'fat': 0.0, 'protein': 0.0},
        {'name': 'Coca-cola', 'calories': 140, 'fat': 0.0, 'protein': 0.0},
        {'name': 'Orange Juice', 'calories': 112, 'fat': 0.5, 'protein': 1.7},
        {'name': 'Water', 'calories': 0, 'fat': 0.0, 'protein': 0.0},
    ]

    for food_data in sample_foods:
        food = Food(
            name=food_data['name'],
            calories=food_data['calories'],
            fat=food_data['fat'],
            protein=food_data['protein']
        )
        db.session.add(food)
    db.session.commit()