from pydoc import text
from app import db
from sqlalchemy import text
from datetime import date, datetime
from flask_mysqldb import MySQL

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable = False)
    email = db.Column(db.String(100),nullable = True)
    password = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(15), nullable=True)
    profile_pic = db.Column(db.String(300), nullable=True, default='static/uploads/profile_pics/default.jpg')
    role = db.Column(db.String(20), default='user')
    dateOfBirth = db.Column(db.Date, nullable=True, default='2000-01-01')
    weight = db.Column(db.Float, nullable=True, default=0.0)
    height = db.Column(db.Float, nullable=True, default=0.0)
    goal = db.Column(db.String(100), nullable=True, default='No specific')
    bmi = db.Column(db.Float, nullable=True, default=0.0)
    bmr = db.Column(db.Float, nullable=True, default=0.0)
    maintenance_calories = db.Column(db.Float, nullable=True, default=0.0)
    total_workout_volume = db.Column(db.Integer, default=0)
    total_reward_score = db.Column(db.Integer, default=0)

    course_enrollments = db.relationship('CourseEnrollment', backref='user', lazy=True, cascade="all, delete-orphan")
    fitness_activities = db.relationship('FitnessActivity', backref='user', lazy=True, cascade="all, delete-orphan")


    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.bmi = self.calculate_bmi()
        self.bmr = self.calculate_bmr()
        self.maintenance_calories = self.calculate_maintenance_calories()

    def calculate_bmi(self):
        if not self.height or not self.weight or self.weight <= 0 or self.height <= 0:
            return 0.0
        return round(self.weight / ((self.height / 100) * (self.height / 100)), 2)
    
    def calculate_bmr(self):
        if not self.height or not self.weight or self.weight <= 0 or self.height <= 0 or not self.dateOfBirth:
            print(self.dateOfBirth,'end')
            return 0.0
        age = 2025 - int(self.dateOfBirth[self.dateOfBirth.rfind('-') + 1:])
        return round(10 * self.weight + 6.25 * (self.height * 100) - 5 * age, 2)

    def calculate_maintenance_calories(self):
        if self.bmr <= 0:
            return 0.0
        return round(self.bmr * 1.2)
        
    @staticmethod
    def find_by_email(email):
        sql = text("SELECT * FROM user WHERE email = email")
        result = db.session.execute(sql, {"email": email}).first()
        return result
    
    def save(self):
        sql = text("""
            INSERT INTO user (name, email, password, phone, role, dateOfBirth, weight, height, goal)
            VALUES (:name, :email, :password, :phone, :role, :dateOfBirth, :weight, :height, :goal)
        """)
        password = User.passwordEncryption(self.password)
        db.session.execute(sql, {
            "name": self.name,
            "email": self.email,
            "password": password,
            "phone": self.phone,
            "role": self.role,
            "dateOfBirth": self.dateOfBirth,
            "weight": self.weight,
            "height": self.height,
            "goal": self.goal
        })
        db.session.commit()
    
    def delete(self):
        sql = text("DELETE FROM user WHERE id = :user_id")
        db.session.execute(sql, {"user_id": self.id})
        db.session.commit()
    
    @staticmethod
    def getUser(id):
        sql = text("SELECT * FROM user WHERE id = :user_id")
        result = db.session.execute(sql, {"user_id": id}).first()
        return result

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'profile_pic': self.profile_pic,
            'role': self.role,
            'dateOfBirth': self.dateOfBirth.isoformat() if self.dateOfBirth else '2001-01-01',
            'weight': self.weight,
            'height': self.height,
            'goal': self.goal,
            'bmi': self.bmi,
            'bmr': self.bmr,
            'maintenance_calories': self.maintenance_calories
        }

    @staticmethod
    def passwordEncryption(password):
        mystring = ''
        for i in password:
            mystring += chr(ord(i) + 3)
        return mystring

    @staticmethod
    def findUser(email):
        return User.query.filter_by(email=email).first()
    
    def get_username(self):
        return self.name
    
    @staticmethod
    def getUser(id):
        return User.query.get(id)

    @staticmethod
    def get_all_ordered_by_score():
        return User.query.order_by(User.total_reward_score.desc()).all()
    
    def update(self, form_data):
        sql = text("""
            UPDATE user SET name = :name, phone = :phone,
                goal = :goal, weight = :weight,
                height = :height, dateOfBirth = :dateOfBirth, bmi = :bmi, bmr = :bmr, maintenance_calories = :maintenance_calories
            WHERE id = :user_id
        """)
        weight = float(form_data.get('weight', 0))
        height = float(form_data.get('height', 0))
        

        self.name = form_data.get('name')
        self.phone = form_data.get('phone')
        self.goal = form_data.get('goal')
        self.weight = weight
        self.height = height
        self.dateOfBirth = form_data.get('dateOfBirth')
        if not self.dateOfBirth:
            self.dateOfBirth = '2000-01-01'
        
        self.bmi = self.calculate_bmi()
        self.bmr = self.calculate_bmr()
        self.maintenance_calories = self.calculate_maintenance_calories()

        db.session.execute(sql, {
            "name": self.name,
            "phone": self.phone,
            "goal": self.goal,
            "weight":  self.weight,
            "height": self.height,
            "dateOfBirth": self.dateOfBirth,
            "user_id": self.id,
            "bmi": self.bmi,
            "bmr": self.bmr,
            "maintenance_calories": self.maintenance_calories
        })


        db.session.commit()