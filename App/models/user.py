from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

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
    name = db.Column(db.String(50), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    current_loc = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(20), nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False, unique=True)

    def __init__(self, name, vehicle_number):
        self.name = name
        self.vehicle_number = vehicle_number
        self.status = 'available'

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'vehicle_number': self.vehicle_number
        }
    

class Drives(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)
    time = db.Column(db.String(20), nullable=True)
    date = db.Column(db.String(20), nullable=True)

    def __init__(self, driver_id, resident_id):
        self.driver_id = driver_id
        self.resident_id = resident_id

    def get_json(self):
        return {
            'id': self.id,
            'driver_id': self.driver_id,
        }


class Stops(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drive_id = db.Column(db.Integer, db.ForeignKey('drives.id'), nullable=False)
    resident_id = db.Column(db.Integer, db.ForeignKey('resident.id'), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    time = db.Column(db.String(20), nullable=True)
    date = db.Column(db.String(20), nullable=True)

    def __init__(self, drive_id, address):
        self.drive_id = drive_id
        self.address = address

    def get_json(self):
        return {
            'id': self.id,
            'drive_id': self.drive_id,
            'address': self.address
        }


class Resident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100), nullable=False)
    street = db.Column(db.String(10), nullable=False)

    def __init__(self, name, address, street):
        self.name = name
        self.address = address
        self.street = street

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
        }