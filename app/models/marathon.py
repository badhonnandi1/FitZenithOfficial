from app import db
from datetime import datetime
from sqlalchemy import text

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
        sql = text("SELECT * FROM marathon ORDER BY date ASC")

        result = db.session.execute(sql).mappings().all()
        return result
    
    @staticmethod
    def get_by_id(marathon_id):
        sql = text("SELECT * FROM marathon WHERE id = :marathon_id")

        result = db.session.execute(sql, {"marathon_id": marathon_id}).mappings().first()
        if not result:
            return None
        return result
    
    @staticmethod
    def create(form_data):
        date_str = form_data.get('date')
        if not date_str:
            return None, "Date is required"


        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M')
        params = {
            "title": form_data.get('title'),
            "date": date,
            "location": form_data.get('location'),
            "price": float(form_data.get('price', 0)),
            "slots": int(form_data.get('slots', 0)),
            "description": form_data.get('description')
        }

        sql = text("""
            INSERT INTO marathon (title, date, location, price, slots, description) VALUES (:title, :date, :location, :price, :slots, :description)""")

        result = db.session.execute(sql, params)
        db.session.commit()


        new_id = result.lastrowid
        return {"id": new_id, **params}, None 

    @staticmethod
    def delete_by_id(marathon_id):
        sql = text("DELETE FROM marathon WHERE id = :marathon_id")
        db.session.execute(sql, {"marathon_id": marathon_id})
        db.session.commit()

class MarathonRegistration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    registration_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    marathon_id = db.Column(db.Integer, db.ForeignKey('marathon.id'), nullable=False)

    
    user = db.relationship('User', backref='marathon_registrations', lazy=True)


    @staticmethod
    def checkRegister(user_id, marathon_id):
        sql = text("SELECT EXISTS(SELECT 1 FROM marathon_registration WHERE user_id = :user_id AND marathon_id = :marathon_id)")
        result = db.session.execute(sql, {"user_id": user_id, "marathon_id": marathon_id}).scalar()
        return result 
    

    @staticmethod
    def register_user(user_id, marathon_id):
        if MarathonRegistration.checkRegister(user_id, marathon_id):
            return False, "Tomar Registration kora Done"

        get_slots_sql = text("SELECT slots FROM marathon WHERE id = :marathon_id FOR UPDATE")
        marathon_slots = db.session.execute(get_slots_sql, {"marathon_id": marathon_id}).scalar()

        if marathon_slots is not None and marathon_slots > 0:
            
            update_slots_sql = text("UPDATE marathon SET slots = slots - 1 WHERE id = :marathon_id")
            db.session.execute(update_slots_sql, {"marathon_id": marathon_id})

            regquery = text(""" INSERT INTO marathon_registration (user_id, marathon_id, registration_time) VALUES (:user_id, :marathon_id, NOW())""")

            db.session.execute(regquery, {"user_id": user_id, "marathon_id": marathon_id})

            db.session.commit()
            
            return True, "Registration Hoye Gece"
        else:
            db.session.rollback() 
            return False, "Jayga nai vai maff kor"
