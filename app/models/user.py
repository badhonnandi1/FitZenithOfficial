from pydoc import text
from app import db
from datetime import date, datetime


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
            return 0.0
        age = date.today().year - self.dateOfBirth.year
        return round(10 * self.weight + 6.25 * (self.height * 100) - 5 * age, 2)

    def calculate_maintenance_calories(self):
        if self.bmr <= 0:
            return 0.0
        return round(self.bmr * 1.2)  
        
    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    @staticmethod
    def getUser(id):
        return User.query.get(id)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'profile_pic': self.profile_pic,
            'role': self.role,
            'dob': self.dob.isoformat() if self.dob else None,
            'weight': self.weight,
            'height': self.height,
            'goal': self.goal,
            'bmi': self.bmi,
            'bmr': self.bmr,
            'maintenance_calories': self.maintenance_calories
        }

    @staticmethod
    def findUser(email):
        return User.query.filter_by(email=email).first()
    
    def get_username(self):
        return self.name
    
    @staticmethod
    def getUser(id):
        return User.query.get(id)
    
    def update(self, form_data):

        self.name = form_data.get('name', self.name)
        self.phone = form_data.get('phone', self.phone)
        self.goal = form_data.get('goal', self.goal)
        
        weight_str = form_data.get('weight')
        if weight_str:
            self.weight = float(weight_str)

        height_str = form_data.get('height')
        if height_str:
            self.height = float(height_str)
        
        dob_str = form_data.get('dob')
        if dob_str:
            self.dateOfBirth = datetime.strptime(dob_str, '%Y-%m-%d').date()

        self.bmi = self.calculate_bmi()
        self.bmr = self.calculate_bmr()
        self.maintenance_calories = self.calculate_maintenance_calories()

        self.save()