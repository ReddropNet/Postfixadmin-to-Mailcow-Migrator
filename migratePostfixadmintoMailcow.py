import mysql.connector, os, requests 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()



#Grab the Environment Variables
mailcow_host = os.environ.get("MAILCOW_HOST")
mailcow_api_key = os.environ.get("MAILCOW_API_KEY")

db_config = {
    'host': os.environ.get("DB_HOST"),
    'port': os.environ.get("DB_PORT"),
    'user': os.environ.get("DB_USER"),
    'password': os.environ.get("DB_PASS"),
    'database': os.environ.get("DB_DB")
}

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-Key": mailcow_api_key
}


# Base Collection Class
class BaseCollection():
    def __init__(self,db_config):
        self.db_config = db_config
        self.items = []
        self.load_data()
    
    def load_data(self):
        raise NotImplementedError("Subclass must implement 'load_data()'")
    
    def get_all(self):
        return self.items
    
# A single alias object
class Alias:
    def __init__(self, address, goto, domain, active):
        self.address = address
        self.goto = goto
        self.domain = domain
        self.active = active
    
    def __repr__(self):
        return f"<Alias {self.address} → {self.goto} ({self.domain}, active={self.active})>"

# Collection of all the Aliases
class Aliases(BaseCollection):
    def load_data(self):
        query = "SELECT address, goto, domain, active FROM alias"
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor.fetchall():
            self.items.append(Alias(*row))

class Domain:
    def __init__(self, domain, description, backupmx, active):
        self.domain = domain
        self.description = description
        self.backupmx = backupmx
        self.active = active
    
    def __repr__(self):
        return f"<Domain {self.domain} ({self.description}, backupmx={self.backupmx}, active={self.active})>"

# Collection of all Domains
class Domains(BaseCollection):
    def load_data(self):
        query = "SELECT domain, description, backupmx, active FROM domain"
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor.fetchall():
            d = Domain(*row)
            if d.domain != "ALL":       #Skip the "ALL" Domain that Mailcow does not need.
                self.items.append(d)

# A Single Mailbox Object
class Mailbox:
    def __init__(self, username, password, name, maildir, local_part, domain, active):
        self.username = username
        self.password = password
        self.name = name
        self.maildir = maildir
        self.local_part = local_part
        self.domain = domain
        self.active = active

    
    def __repr__(self):
        return f"<Mailbox {self.username} ({self.name}, password={self.password}, active={self.active})>"

#Collection of all Mailboxes
class Mailboxes(BaseCollection):
    def load_data(self):
        query = "SELECT username, password, name, maildir, local_part, domain, active FROM mailbox"
        connection = mysql.connector.connect(**self.db_config)
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor.fetchall():
            self.items.append(Mailbox(*row))

#Extract domains from postfixadmin DB and insert into MailCow via API
def migrate_domains(db_config,mailcow_host,headers):
    url = mailcow_host + "/api/v1/add/domain"
    domain_table = Domains(db_config)
    for d in domain_table.get_all():
        print(d)
        data = {
            "active": d.active,
            "backupmx": d.backupmx,
            "description": d.description,
            "domain": d.domain
        }
        response = requests.post(url,json=data, headers=headers, verify=False)
        if response.status_code == 200:
            print(f'Added domain {d.domain}')
        else:
            print(response.status_code)
            print(response.text)  

def migrate_mailboxes(db_config,mailcow_host,headers):
    url = mailcow_host + "/api/v1/add/mailbox"
    mailbox_table = Mailboxes(db_config)
    for m in mailbox_table.get_all():
        print(m)
        data = {
            "active": m.active,
            "domain": m.domain,
            "local_part": m.local_part,
            "name": m.name,
            "password": "{MD5-CRYPT}" + m.password,
            "password2": "{MD5-CRYPT}" + m.password,
            "use_pw_hash": 1
        }
        response = requests.post(url,json=data, headers=headers, verify=False)
        if response.status_code == 200:
            print(f'Added mailbox {m.local_part}@{m.domain}')
        else:
            print(response.status_code)
            print(response.text)  

def migrate_aliases(db_config,mailcow_host,headers):
    url = mailcow_host + "/api/v1/add/alias"
    alias_table = Aliases(db_config)
    for a in alias_table.get_all():
        data = {
            "active": a.active,
            "address": a.address,
            "goto": a.goto
        }
        if a.address.rstrip().lower() == a.goto.rstrip().lower():
            print(f"Skpping {a.address} -> {a.goto} not neeeded in MailCow!!!")
        else:
            response = requests.post(url,json=data, headers=headers, verify=False)
            if response.status_code == 200:
                print(f'Added Alias {a.address} -> {a.goto}')
            else:
                print(response.status_code)
                print(response.text)  


        
# --- Main Execution ---
if __name__ == "__main__":
    print(f'{mailcow_host}: {mailcow_api_key}')
    migrate_domains(db_config,mailcow_host,headers)
    migrate_mailboxes(db_config,mailcow_host,headers)
    migrate_aliases(db_config,mailcow_host,headers)


