# Bread Van App CLI Commands

# Initializing the Database
Before executing any of the CLI commands, we must initialize  the database with the required objects.

```bash
$ flask init
```

# Driver Commands

## Schedule a Drive to a Street
This command allows a driver to login and proceed to schedule a driver on a specified street at a specific date and time in the database.

**Please login using the username "Trudy" and password "trudypass".**
```bash
$ flask driver schedule Main Street 14:00 29-10-2025
```

## Update Driver Status and Location
This command allows a driver to login and proceed to update their current status and location to the specified parameters in the database.

**Please login using the username "Trudy" and password "trudypass".**
```bash
$ flask driver update Working Main Street
```

# Resident Commands

## View Inbox of Scheduled Drives
This command allows a resident to login and view all scheduled driver for their street in the database.

**Please login using the username "Bob" and password "bobpass".**
```bash
$ flask resident inbox
```

## View Driver Status and Location
This command allows a resident to login and view the status and location of a driver for a scheduled drive on their street in the database.

**Please login using the username "Bob" and password "bobpass".**
```bash
$ flask resident status 1
```

## Request a Stop for a Drive
This command allows a resident to login and request a stop for a scheduled drive on their street in the database.

**Please login using the username "Bob" and password "bobpass".**
```bash
$ flask resident request 1
```