# Postfixadmin-to-Mailcow-Migrator

Easily migrate your PostfixAdmin configuration and mail data to Mailcow with minimal hassle.

This project was created because transitioning to Mailcow was significantly simpler than trying to keep PostfixAdmin configurations working with the major changes in Debian 12/13 and modern Dovecot versions. These scripts automate the migration process, saving you hours of manual work.

##  Features
- Migrate PostfixAdmin data → Mailcow via API
- Maildir migration helper script to move existing mailboxes
- Simple setup with Python virtual environment
- Works great with Mailcow’s Dockerized environment


## Prerequisites
- Python 3.8+
- Access to the PostfixAdmin database (MySQL/MariaDB)
- A running Mailcow instance (and an API key)
- Shell access to the server(s) hosting your Maildir data (optional but recommended)

## Installation:

```
git clone https://github.com/ReddropNet/Postfixadmin-to-Mailcow-Migrator.git
cd Postfixadmin-to-Mailcow-Migrator
python3 -m venv .venv
source .venv/bin/activate
pip3 -r requirements.txt
```

## Configuration:
Copy the sample environment file and update it with your values:
```
cp env.sample .env
```

Then edit .env with your details:

```
export DB_HOST=127.0.0.1
export DB_USER=root
export DB_PASS=SUPERSECRETPASSWORD
export DB_PORT=13306
export DB_DB=postfixadmin
export MAILCOW_HOST=https://mail.example.com/
export MAILCOW_API_KEY=SUPERSECRETAPIKEY
```

## Usage
Run the main migration script:
```
python3 ./migratePostfixadmintoMailcow.py
```

## Optional: Maildir Migration
Optional: Maildir Migration
Move the postfixadmin Maildir in the root of each users home contents into a proper Maildir/ subfolder
```
./migrateMailDir.sh
```

## Troubleshooting
- Ensure your Mailcow API key has admin privileges.
- Check MySQL connectivity:
```
mysql -h $DB_HOST -u $DB_USER -p$DB_PASS $DB_DB
```
