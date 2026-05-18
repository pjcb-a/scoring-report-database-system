<!-- CONNECTION FLOW -->
<!-- Computer 2 (Vue Frontend)
        │
        │ API Requests
        ▼ -->
http://192.168.x.x:5000

<!-- Computer 1
 ├── Flask Backend
 └── PostgreSQL
PostgreSQL Configuration

In PostgreSQL: -->

postgresql.conf

<!-- Enable external connection: -->

listen_addresses = '*'

pg_hba.conf
<!-- Allow local network access: -->

host    all    all    192.168.1.0/24    md5

<!-- Flask Database URI -->
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost/sports_db"