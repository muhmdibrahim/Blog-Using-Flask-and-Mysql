from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_mysqldb import MySQL
from flask_sqlalchemy import SQLAlchemy
import MySQLdb.cursors
import re 

app = Flask(__name__)
app.secret_key = 'hemaaai12341234'

# Enter your database connection details below
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = 'hemaa_ai'
app.config['MYSQL_PASSWORD'] = 'hemaa1234' 
app.config['MYSQL_DB'] = 'login_user'

mysql = MySQL(app)


# http://localhost:5000/pythonlogin/ - this will be the login page, 
# we need to use both GET and POST requests
@app.route('/pythonlogin/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password))
        # Fetch one record and return result
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']
            
            return redirect(url_for('home'))
        else:
            flash("Incorrect username/password!", "danger")
    return render_template('auth/login.html',title="Login")


# http://localhost:5000/pythonlogin/register 
# This will be the registration page, we need to use both GET and POST requests
@app.route('/pythonlogin/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute( "SELECT * FROM accounts WHERE username = %s", (username,) )
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            flash("Account already exists!", "danger")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid email address!", "danger")
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash("Username must contain only characters and numbers!", "danger")
        elif not username or not password or not email:
            flash("Incorrect username/password!", "danger")
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, NULL)', (username, password, email))
            mysql.connection.commit()
            flash("You have successfully registered!", "success")
            return redirect(url_for('login'))

    elif request.method == 'POST':
        flash("Please fill out the form!", "danger")

    return render_template('auth/register.html',title="Register")

# http://localhost:5000/pythinlogin/home 

# check session for each page

@app.route('/')
def home():
    if 'loggedin' in session:
        return render_template('home/home.html', username=session['username'],title="Home")
    return redirect(url_for('login'))    

@app.route('/blog')
def blog():
    if 'loggedin' in session:
        return render_template('blog/blog.html', username=session['username'], title="Blog")
    return redirect(url_for('login'))  

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
   # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('login'))

@app.route('/pythonlogin/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == "POST":
        text = request.form.get('text_cr_post')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if 'loggedin' in session:
                #cursor.execute('UPDATE post SET text = %s WHERE author = %s', (text, session['id'],))
                cursor.execute('INSERT INTO post VALUES(NULL, %s, %s, %s)', (text, session['id'], session['username'], ))
                mysql.connection.commit()
                #flash('Post created!', category='success')
                return redirect(url_for('create_post'))

    return render_template('blog/create_post.html', username = session['username'], title="Create Post")

#from models import accounts, post, comments, likes

@app.route("/pythonlogin/postat")
def postat():
    #postat = post.query.filter_by(author = 2)
    if 'loggedin' in session:
        user = session['username']

        if not user:
            return redirect(url_for('home'))
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM post')
        posts = cursor.fetchall()
        cursor.execute('SELECT * FROM comments')
        comments = cursor.fetchall()

    return render_template("blog/posts.html", comments = comments, user = session['id'], posts= posts, username=user)

@app.route("/pythonlogin/delete_post/<id>")
def delete_post(id):
    #id = int(request.form("post_id"))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if 'loggedin' in session:
        cursor.execute('DELETE FROM post WHERE id = %s', (id,))
        mysql.connection.commit()
        
        return redirect(url_for('postat'))

@app.route("/pythonlogin/create_comment/<id>", methods=['GET', 'POST'])
def create_comment(id):
    if request.method == "POST":
        text = request.form.get('text_cr_comment')

        if not text:
            flash('Post cannot be empty', category='error')
        else:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if 'loggedin' in session:
                cursor.execute('INSERT INTO comments VALUES(NULL, %s, %s, %s)', (text, session['id'], id, ))
                mysql.connection.commit()
    return redirect(url_for('postat'))

@app.route("/pythonlogin/delete_comment/<id>")
def delete_comment(id):
    #id = int(request.form("post_id"))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if 'loggedin' in session:
        cursor.execute('DELETE FROM comments WHERE id = %s', (id,))
        mysql.connection.commit()
        
        return redirect(url_for('postat'))
    
@app.route("/pythonlogin/delete_user/<name>")
def delete_user(name):
    #id = int(request.form("post_id"))
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if 'loggedin' in session:
        cursor.execute('DELETE FROM accounts WHERE username = %s', (name,))
        mysql.connection.commit()
        
        return redirect(url_for('admin'))

@app.route("/pythonlogin/admin")
def admin():
    if 'loggedin' in session:
        if session['id'] == 1:
            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM post')
            posts = cursor.fetchall()
            cursor.execute('SELECT * FROM comments')
            comments = cursor.fetchall()
            cursor.execute('SELECT * FROM accounts')
            accounts = cursor.fetchall()
            return render_template('auth/admin.html',comments = comments, accounts = accounts,
                                    posts= posts, username=session['username'], user = session['id'], title="Admin")
    return redirect(url_for('login')) 

@app.route("/pythonlogin/layout")
def layout():
    if 'loggedin' in session:
        return render_template('home/layout.html', username=session['username'],title="Layout")
    return redirect(url_for('login')) 

if __name__ =='__main__':
	app.run(debug=True)
