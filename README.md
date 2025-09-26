# Postfixadmin-to-Mailcow-Migrator

Migration Script from postfixadmin to MailCow

## Installation:

```
python3 -m venv .venv
source .venv/bin/activate
pip3 -r requirements.txt
```
## Usage:
```
mv env.sample .env
```


### Set your environment variables
.env
```
export DB_HOST=127.0.0.1
export DB_USER=root
export DB_PASS=SUPERSECRETPASSWORD
export DB_PORT=13306
export DB_DB=postfixadmin
export MAILCOW_HOST=https://mail.example.com/
export MAILCOW_API_KEY=SUPERSECRETAPIKEY
```

### Run the script
```
python3 ./migratePostfixadmintoMailcow.py
```

### Optional
Run the migrateMailDir.sh to move the mail into a per user .Maildir/ folder

BASE="/var/lib/docker/volumes/mailcowdockerized_vmail-vol-1/_data"