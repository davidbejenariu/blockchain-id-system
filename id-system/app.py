from flask import Flask, render_template, session, redirect, url_for, request
from flask_mysqldb import MySQL
from forms import *
from sql_helpers import *
import qrcode

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'bLocKcHAin'
app.config['MYSQL_DB'] = 'blockchain-id-system'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['SECRET_KEY'] = 'secret123'

mysql = MySQL(app)


def log_in_user(email):
    users = Table('user', 'name', 'email', 'password', 'role')
    user = users.get_one('email', email)

    session['logged_in'] = True
    session['email'] = email
    session['name'] = user.get('name')
    session['role'] = user.get('role')
    session['qr_generated'] = user.get('qr_generated')
    # TODO new get function for user block in blockchain


@app.route('/')
def index():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    elif session['role'] == 'admin':
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))


@app.route('/dashboard/admin', methods=['GET', 'POST'])
def admin_dashboard():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))
    elif 'role' not in session or session['role'] == 'default':
        return redirect(url_for('user_dashboard'))

    users = Table('user', 'name', 'email', 'password', 'role')
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.form)

        if form.validate():
            name = form.name.data
            email = form.email.data
            password = form.password.data
            is_admin = form.is_admin.data

            if is_admin:
                role = 'admin'
            else:
                role = 'default'

            users.insert(name, email, password, role)

    return render_template('admin_dashboard.html', form=form, session=session)


@app.route('/dashboard')
def user_dashboard():
    if 'logged_in' not in session or not session['logged_in']:
        return redirect(url_for('login'))

    if session['qr_generated'] == 0:
        # Add user to blockchain
        blockchain = get_blockchain()
        data = f"{session['name']},{session['email']}"

        blockchain.mine(Block(data=data))
        sync_blockchain(blockchain)

        users = Table('user', 'name', 'email', 'password', 'role', 'qr_generated')
        users.set_one(session['email'], 'qr_generated', '1')

        # Encoding data using make() function
        qr = qrcode.make(data)
        qr.save(f"static/QRs/{session['name']}.png")

        session['qr'] = f"QRs/{session['name']}.png"
        session['qr_generated'] = 1


    return render_template('user_dashboard.html', session=session)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session and session['logged_in']:
        return redirect(url_for('user_dashboard'))

    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.form)

        if form.validate():
            email = form.email.data
            password = form.password.data

            users = Table('user', 'name', 'email', 'password', 'role')
            user = users.get_one('email', email)

            try:
                acc_pass = user.get('password')
            except:
                return render_template('login.html', form=form, session=session)

            # nobody's gonna know
            if acc_pass == password:
                # they're gonna know
                log_in_user(email)
                return redirect(url_for('user_dashboard'))

    return render_template('login.html', form=form, session=session)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
