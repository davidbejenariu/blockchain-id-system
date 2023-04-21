from flask import Flask
from flask_mysqldb import MySQL
from sql_helpers import *


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'bLocKcHAin'
app.config['MYSQL_DB'] = 'blockchain-id-system'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'secret123'

mysql = MySQL(app)

