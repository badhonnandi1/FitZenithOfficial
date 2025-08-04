from app import db
from datetime import datetime

class Marathon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0.0)
    slots = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_path = db.Column(db.String(300), nullable=True, default='images/default_marathon.jpg')
    

    #ekhane 1 to many relationship with MarathonRegistration use korchi
    registrations = db.relationship('MarathonRegistration', backref='marathon', lazy=True, cascade="all, delete-orphan")


    @staticmethod
    def get_all():
        return Marathon.query.order_by(Marathon.date.asc()).all()

    @staticmethod
    def get_by_id(marathon_id):
        return Marathon.query.get_or_404(marathon_id)

    @staticmethod
    def create(form_data):
        date_str = form_data.get('date')
        if not date_str:
            return None, "Date is required"
        
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        new_marathon = Marathon(
            title=form_data.get('title'),
            date=date,
            location=form_data.get('location'),
            price=float(form_data.get('price', 0)),
            slots=int(form_data.get('slots', 0)),
            description=form_data.get('description')
        )
        db.session.add(new_marathon)
        db.session.commit()
        return new_marathon, None


class MarathonRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    marathon_id = db.Column(db.Integer, db.ForeignKey('marathon.id'), nullable=False)


    @staticmethod
    def checkRegister(user_id, marathon_id):
        return MarathonRegistration.query.filter_by(user_id=user_id, marathon_id=marathon_id).first() is not None

    @staticmethod
    def register_user(user_id, marathon_id):
        marathon = Marathon.get_by_id(marathon_id)

        if MarathonRegistration.checkRegister(user_id, marathon_id):
            return False, "Tomar Registration kora Done"

        if marathon.slots <= 0:
            return False, "Jayga nai vai maff kor"
        else:
            marathon.slots -= 1
            new_registration = MarathonRegistration(user_id=user_id, marathon_id=marathon_id)
            db.session.add(new_registration)
            db.session.commit()
            return True, "Registration Hoye Gece"

