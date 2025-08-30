from app import db
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import selectinload

class Marathon(db.Model):

    __tablename__ = 'marathon'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    slots = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(300), nullable=True, default='images/default_marathon.jpg')
    
    registrations = db.relationship('MarathonRegistration', backref='marathon', lazy=True, cascade="all, delete-orphan")

    @staticmethod
    def get_all():
        return Marathon.query.order_by(Marathon.date.asc()).all()
    
    @staticmethod
    def get_by_id(marathon_id):
        return Marathon.query.get(marathon_id)
    
    @staticmethod
    def create(form_data):
        date_str = form_data.get('date')
        if not date_str:
            return None, "Date is required"
        else:
            marathon_date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
            new_marathon = Marathon(
            title=form_data.get('title'),
            date=marathon_date,
            location=form_data.get('location'),
            price=float(form_data.get('price', 0)),
            slots=int(form_data.get('slots', 0)),
            description=form_data.get('description')
            )
            db.session.add(new_marathon)
            db.session.commit()
            return new_marathon, None

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class MarathonRegistration(db.Model):

    __tablename__ = 'marathon_registration'

    id = db.Column(db.Integer, primary_key=True)
    registration_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    marathon_id = db.Column(db.Integer, db.ForeignKey('marathon.id'), nullable=False)

    user = db.relationship('User', backref='marathon_registrations', lazy=True)


    @staticmethod
    def checkRegister(user_id, marathon_id):

        result = MarathonRegistration.query.filter_by(user_id=user_id, marathon_id=marathon_id).first() 
        return True if result else False

    @staticmethod
    def register_user(user_id, marathon_id):
 
        if MarathonRegistration.checkRegister(user_id, marathon_id):
            return False, "Tomar Registration kora Done"

        marathon_to_update = Marathon.query.filter_by(id=marathon_id).with_for_update().first()
        
        if marathon_to_update and marathon_to_update.slots > 0:
            marathon_to_update.slots -= 1
            new_registration = MarathonRegistration(user_id=user_id, marathon_id=marathon_id)
            db.session.add(new_registration)
            db.session.commit()
            return True, "Registration Done"
        else:
            return False, "Slot Full"
