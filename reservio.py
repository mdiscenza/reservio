"""
 Reservio
    ~~~~~~
    A web-based reservation system for restaurats that pages customers with texts when their tables are ready.
    Indeed, this is closely based on Flaskr... baby steps
    Written in flask for ADI's DevFest 2013 by Michael Discenza

    sqlite3 /tmp/reservio.db < schema.sql


"""
from __future__ import with_statement
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack
from twilio.rest import TwilioRestClient
from config import account_sid, auth_token, secret_key, username, password 
#imports private tokens for my Twillio account and for this app


# app configuration
DATABASE = '/tmp/reservio.db'
DEBUG = True
SECRET_KEY = secret_key
USERNAME = username
PASSWORD = password

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)








def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db


@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


@app.route('/')
@app.route('/<partysize>')
def show_entries(partysize=None):
    if partysize==None:
        db = get_db()
        cur = db.execute('select name, cellnumber, partyof, priority, id from entries order by id asc')
        entries = cur.fetchall()
    else:
        query = ("select name, cellnumber, partyof, priority from entries where partyof=%d order by id asc" % int(partysize))
        db = get_db()
        cur = db.execute(query)
        entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)



@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    name = request.form['name']
    cellnumber = request.form['cellnumber']
    partyof = request.form['partyof']
    try: #yes this is indeed the hackiest way ever to do this, but it works
        priority = request.form['priority']
        priority = 1
    except KeyError:
        priority = 0
    print (priority)
    db.execute('insert into entries (name, cellnumber, partyof, priority) values (?, ?, ?, ?)', [name, cellnumber, partyof, priority])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

@app.route('/text/<reservation_id>')
def text(reservation_id):
    client = TwilioRestClient(account_sid, auth_token)
    db = get_db()
    recipiant_number = db.execute("select cellnumber from entries where id= %s" % reservation_id).fetchone()[0]
    recipiant_name = db.execute("select name from entries where id= %s" %reservation_id).fetchone()[0]
    message_body = "Hey %s, your table is ready! Please see the host right away!" %str(recipiant_name)
    message = client.sms.messages.create(to=("+%s" % recipiant_number), from_="+18602544361",body=message_body)
    print message.sid
    flash('Your text was sent!')
    return redirect(url_for('show_entries'))





if __name__ == '__main__':
    init_db()
    app.run(debug=True)
