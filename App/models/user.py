from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)


class Driver(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    current_loc = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    plate_number = db.Column(db.String(20), nullable=False, unique=True)

    def __init__(self, username, password, contact, status, plate_number, current_loc):
        self.username = username
        self.password = generate_password_hash(password)
        self.contact = contact
        self.status = status
        self.plate_number = plate_number
        self.current_loc = current_loc

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'contact': self.contact,
            'current_loc': self.current_loc,
            'status': self.status,
            'plate_number': self.plate_number
        }
    
    def get_contact(self):
        return {
            'username': self.username,
            'contact': self.contact
        }

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def update_driver(self, status, current_loc):
        self.status = status
        self.current_loc = current_loc
        db.session.commit()


class Drives(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=False)
    time = db.Column(db.Time, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def __init__(self, driver_id, time_str, date_str, street_id):
        self.driver_id = driver_id
        self.time = datetime.strptime(time_str, '%H:%M').time()
        self.date = datetime.strptime(date_str, '%d-%m-%Y').date()
        self.street_id = street_id

    def get_json(self):
        return {
            'id': self.id,
            'driver_id': self.driver_id,
            'time': self.time.strftime("%H:%M"),
            'date': self.date.strftime("%Y-%m-%d"),
            'street_id': self.street_id
        }


class Stops(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('drives.id'), nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'), nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(20), nullable=True)
    date = db.Column(db.String(20), nullable=True)

    def __init__(self, drive_id, resident_id, street_id, address, time, date):
        self.drive_id = drive_id
        self.resident_id = resident_id
        self.street_id = street_id
        self.time = time
        self.date = date
        self.address = address

    def get_json(self):
        return {
            'id': self.id,
            'drive_id': self.drive_id,
            'resident_id': self.resident_id,
            'street_id': self.street_id,
            'time': self.time,
            'date': self.date,
            'address': self.address
        }


class Street(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    street_name = db.Column(db.String(10), nullable=False)
    city = db.Column(db.String(50), nullable=False)

    def __init__(self, street_name, city):
        self.street_name = street_name
        self.city = city

    def get_json(self):
        return {
            'id': self.id,
            'street_name': self.street_name,
            'city': self.city
        }


class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    street_id = db.Column(db.Integer, db.ForeignKey('street.id'), nullable=False)

    def __init__(self, username, password, address, contact, street_id):
        self.username = username
        self.password = generate_password_hash(password)
        self.address = address
        self.contact = contact
        self.street_id = street_id

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'address': self.address,
            'contact': self.contact,
            'street_id': self.street_id
        }
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    