import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User, Driver, Drives, Street, Resident
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    db.drop_all()
    db.create_all()
    db.session.add(Street(street_name='Main Street', city='Springfield'))
    db.session.add(Street(street_name='2nd Street', city='Bakersfield'))
    db.session.add(Street(street_name='3rd Street', city='Hikersfield'))
    db.session.add(Driver(username='Trudy', password='trudypass', contact='8684567890', status='available', plate_number='DGR435', current_loc='HQ'))
    db.session.add(Driver(username='Joe', password='joepass', contact='8683456456', status='available', plate_number='JDF765', current_loc='HQ'))
    db.session.add(Resident(username='Bob', password='bobpass', contact='8684562344', address='123 Main Street, Springfield', street_id=1))
    db.session.add(Resident(username='Alice', password='alicepass', contact='8686756345', address='456 2nd Street, Bakersfield', street_id=2))
    db.session.add(Resident(username='Eve', password='evepass', contact='8685467435', address='789 2nd Street, Bakersfield', street_id=2))
    db.session.commit()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)



resident_cli = AppGroup('resident', help='Resident object commands')

@resident_cli.command("list", help="Lists residents in the database")
def list_residents_command():
    residents = Resident.query.all()
    for resident in residents:
        print(resident.get_json())

@resident_cli.command("inbox", help="Lists all drives scheduled for a resident's street in the database")
def inbox_resident_command():
    print("Please Enter your Resident username: ")
    username = input()
    print("Please Enter your Resident password: ")
    password = input()
    resident = Resident.query.filter_by(username=username).first()
    if resident and resident.check_password(password):
        drives = Drives.query.filter_by(street_id=resident.street_id).all()
        if drives:
            for drive in drives:
                print(drive.get_json())
        else:
            print(f"No drives scheduled for Resident {username}'s street.")
            print("Please contact any of the following drivers to request a drive to your street:")
            drivers=Driver.query.all()
            for driver in drivers:
                print(driver.get_contact())
    else:
        print("Invalid username or password.")

@resident_cli.command("status", help="Allows a resident to check a driver's status and location for a driver to their street in the database")
@click.argument("drive_id", type=int)
def driver_status_resident_command(drive_id):
    print("Please Enter your Resident username: ")
    username = input()
    print("Please Enter your Resident password: ")
    password = input()
    resident = Resident.query.filter_by(username=username).first()
    if resident and resident.check_password(password):
        drive = Drives.query.filter_by(id=drive_id).first()
        if drive:
            driver = Driver.query.filter_by(id=drive.driver_id).first()
            if driver:
                print(f"Driver {driver.username}'s status is {driver.status} and current location is {driver.current_loc}.")
            else:
                print("Driver not found.")
        else:
            print("Unable to retrieve driver status and location without a scheduled drive.")
            print("Please contact any of the following drivers to request a drive to your street:")
            drivers=Driver.query.all()
            for driver in drivers:
                print(driver.get_contact())
    else:
        print("Invalid username or password.")

app.cli.add_command(resident_cli)



driver_cli = AppGroup('driver', help='Driver object commands')

@driver_cli.command("list", help="Lists drivers in the database")
def list_drivers_command():
    drivers = Driver.query.all()
    for driver in drivers:
        print(driver.get_json())

@driver_cli.command("update", help="Updates a driver's status and location in the database")
@click.argument("status", type=str)
@click.argument("current_loc", type=str)
def update_driver_command(status, current_loc):
    print("Please Enter your Driver username: ")
    username = input()
    print("Please Enter your Driver password: ")
    password = input()
    driver = Driver.query.filter_by(username=username).first()
    if driver and driver.check_password(password):
        driver.update_driver(status, current_loc)
        print(f"Driver {username}'s status updated to {status} and location updated to {current_loc}.")
    else:
        print("Invalid username or password.")

@driver_cli.command("schedule", help="Schedules a Drive to a Street for a Driver in the database")
@click.argument("street_name", nargs=-1, type=str)
@click.argument("time", type=str)
@click.argument("date", type=str)
def schedule_drive_command(street_name, time, date):
    print("Please Enter your Driver username: ")
    username = input()
    print("Please Enter your Driver password: ")
    password = input()
    street_name = ' '.join(street_name)
    driver = Driver.query.filter_by(username=username).first()
    street = Street.query.filter_by(street_name=street_name).first()
    if driver and driver.check_password(password):
        if street:
            db.session.add(Drives(driver_id=driver.id, street_id=street.id, time_str=time, date_str=date))
            db.session.commit()
            print(f"Drive scheduled for Driver {username} to {street_name} on {date} at {time}.")
        else:
            print(f"Street {street_name} not found.")
    else:
        print("Invalid username or password.")

app.cli.add_command(driver_cli)


drive_cli = AppGroup('drive', help='Driver object commands')
@drive_cli.command("list", help="Lists drives in the database")
def list_drives_command(): 
    drives = Drives.query.all()
    for drive in drives:
        print(drive.get_json())

app.cli.add_command(drive_cli)