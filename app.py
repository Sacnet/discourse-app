from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
from flask_mysqldb import MySQL
from pymysql.converters import escape_string as thwart
from datetime import timedelta, datetime
import hashlib as hash
from functools import wraps
import mariadb

app = Flask(__name__)
main = Blueprint('main', __name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'discoursemm'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.secret_key= 'discapp'

mysql = MySQL(app)
# Home page route
@app.route('/', methods = ['POST', 'GET'])
def index():
    resultssa=[]
    search=""
    if request.method == 'POST':
        search = request.form['search']
        if search:
            pattern = '%' + search + '%'
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM discoursetext WHERE fullStatement LIKE %s", ('%' + search + '%',))
            resultssa = cur.fetchall()
    return render_template('index.html', resultssa=resultssa, search=search)


# About page route
@app.route('/about')
def about():
    return render_template('about.html')

# Example of handling a form submission

def user_role_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            if session['role']=="admin":
                return f(*args, **kwargs)
            else:
                flash('You dont have privilege to access this page!','danger')
                return render_template("404.html") 
        else:
            flash('Unauthorized, Please login!','danger')
            return redirect(url_for('index'))
    return wrap

@app.route('/updaterole/<id>', methods = ['POST', 'GET'])
@user_role_admin
def updaterole_id(id):
    if request.method == 'POST':
        name = request.form['name']
        userole = request.form['role']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users SET role = %s WHERE id = %s", (thwart(userole), thwart(id),))
        mysql.connection.commit()
        flash('User role updated successfully')
        return redirect(url_for('admin_index'))


def user_role_officer(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            if session['role']=="researcher":
                return f(*args, **kwargs)
            else:
                flash('You dont have privilege to access this page!','danger')
                return render_template("404.html") 
        else:
            flash('Unauthorized, Please login!','danger')
            return redirect(url_for('index'))
    return wrap

def user_role_nrfstaff(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            if session['role']=="nrfuser":
                return f(*args, **kwargs)
            else:
                flash('You dont have privilege to access this page!','danger')
                return render_template("404.html") 
        else:
            flash('Unauthorized, Please login!','danger')
            return redirect(url_for('index'))
    return wrap

@app.route('/text_note',  methods=['GET','POST'])
@user_role_officer
def text_note():
    if request.method == 'POST':
        search = request.form['search']
        fname=session['email']
        date = datetime.now()
        cur = mysql.connection.cursor()
        ar = cur.execute('INSERT INTO textarch(fullTxt, submitted, created_on) values(%s, %s, %s)', (search, fname, date))
        mysql.connection.commit()
        if ar > 0:
            flash("Discourse text submitted for further processing.")
            return  redirect(url_for('text_note'))
        else:
            flash("Error Occurred!")
            return  redirect(url_for('text_note'))
            cur.close()
            session.clear()
    return render_template('text_index.html')

@app.route('/assessor_index',  methods=['GET','POST'])
@user_role_officer
def assessor_index():
    resultssa=[]
    search=""
    if request.method == 'POST':
        search = request.form['search']
        if search:
            pattern = '%' + search + '%'
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM discoursetext WHERE fullStatement LIKE %s", ('%' + search + '%',))
            resultssa = cur.fetchall()
            if resultssa==0:
                fname=session['email']
                date = datetime.now()
                ar = cur.execute('INSERT INTO textarch(fullTxt, submitted, created_on) values(%s, %s, %s)', (search, fname, date))
                mysql.connection.commit()
                if ar > 0:
                    flash("Discourse text not currently in the database but submitted for further processing.")
                    return  redirect(url_for('assessor_index'))
                else:
                    flash("Error Occurred!")
                    return  redirect(url_for('assessor_index'))
                cur.close()
                session.clear()
    return render_template('researcher_index.html', resultssa=resultssa, search=search)


@app.route('/roleedit/<id>', methods = ['POST', 'GET'])
@user_role_admin
def user_id(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (thwart(id),))
    data = cur.fetchall()
    cur.close()
    return render_template('roleedit.html', roleedit=data[0])

@app.route('/accedit/<id>', methods = ['POST', 'GET'])
@user_role_admin
def getuser_id(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (thwart(id),))
    resultasa = cur.fetchone()
    if resultasa['statuss']==0:
        cur.execute("UPDATE users SET status = 1 WHERE id = %s", id)
        flash('Member account activated')
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('admin_index'))
    else:
        cur.execute("UPDATE users SET status=0 WHERE id = %s", (thwart(id),))
        flash('Member account suspended')
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('admin_index'))


@app.route('/admin_index')
@user_role_admin
def admin_index():
    cur = mysql.connection.cursor()
    resultssa = cur.execute("SELECT * FROM users ORDER BY created_on DESC")
    if resultssa > 0:
        cresultsa = cur.fetchall()
        cur.close()
        return render_template('adminpossed_index.html', crustat=cresultsa)
    else:
        flash("No Member to be displayed. Thanks")
        return render_template('adminpossed_index.html')

@app.route('/text_index')
@user_role_admin
def text_index():
    cur = mysql.connection.cursor()
    resultssa = cur.execute("SELECT * FROM textarch ORDER BY created_on DESC")
    if resultssa > 0:
        cresultsa = cur.fetchall()
        cur.close()
        return render_template('textpossed_index.html', crustat=cresultsa)
    else:
        flash("No Member to be displayed. Thanks")
        return render_template('textpossed_index.html')

@app.route('/lpnewpwd', methods=['GET','POST'])
def lpnewpwd():
	if request.method == 'POST':
		npwd = request.form['npwd']
		cpwd = request.form['cpwd']
		slpemail = session['seslpemail']
		if(npwd == cpwd ):
			cur = mysql.connection.cursor()
			cur.execute('UPDATE users set password = %s where email = %s', (npwd, slpemail))
			mysql.connection.commit()
			cur.close()
			session.clear()
			return render_template('login.html',success="Your password was successfully changed.")
		else:
			return render_template('login.html',error="Password doesn't matched.")
	return render_template('lpnewpwd.html')


@app.route('/login',  methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password_candidate = request.form['password']
        cur = mysql.connection.cursor()
        NPasswords = hash.md5(password_candidate.encode())
        LPassword=NPasswords.hexdigest()
        results1 = cur.execute('SELECT * FROM users where email = %s', (thwart(email),))
        if results1 > 0:
            cresults = cur.fetchone()
            password = cresults['password']
            ids = cresults['id']
            surname = cresults['fullname']
            email = cresults['email']
            institution = cresults['institution']
        
            type = cresults['role']
            if password == LPassword:
                session['logged_in'] = True
                session['id'] = ids
                session['email'] = email
                session['surname'] = surname
                session['institution'] = institution
                session['role'] = type
                if type == "user":
                    return redirect(url_for('pinvesti_index'))
                elif type== "researcher":
                    return redirect(url_for('assessor_index'))
                else:
                    return redirect(url_for('admin_index'))
            else:
                error = 'You have entered Invalid password'
                return render_template('login.html', error=error)
            cur.close()
        else:
            error = 'Email was not found or Account block! Contact the Admin to unblock your account'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/logout', methods=["GET", "POST"])
def logout():
	cur = mysql.connection.cursor()
	#lbr = cur.execute('UPDATE profile set user_login = 0 where email = %s',(thwart(session['email']),))
	#mysql.connection.commit()
	#if lbr > 0:
	session.clear()
	return "success"
	#else:
	#return "error"

@app.route('/register', methods=['GET','POST'])
def register():
    global consistent_index
    if request.method == 'POST':
        title = request.form['title']
        surname = request.form['surname']
        othernames = request.form['othernames']
        email = request.form['email']
        phoneno = request.form['phoneno']
        gender = request.form['gender']
        qualif = request.form['qualif']
        field = request.form['field']
        institution = request.form['inst']
        area = request.form['area']
        password = request.form['password']
        compassword = request.form['conpassword']
        
        if (password==compassword):
            date = datetime.now()
            dbPasswords = hash.md5(password.encode())
            NPassword=dbPasswords.hexdigest()
            cur = mysql.connection.cursor()
            fullname=surname+" "+othernames
            cur = mysql.connection.cursor()
            resultssa = cur.execute("SELECT * FROM users WHERE email = %s", (thwart(email),))
            if resultssa > 0:
                flash("You have an already existing account with us, Please login.")
                return redirect(url_for('index'))
            else:
                ar = cur.execute('INSERT INTO users(title, fullname, email, phoneno, gender, qualification, field, institution, area, password, created_on) values(%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s)', (title, fullname, email, phoneno, gender, qualif, field, institution, area, NPassword, date))
                mysql.connection.commit()
                if ar > 0:
                    flash("Thanks for registering! Data sucessfully submitted!.")
                    return  redirect(url_for('index'))
                else:
                    flash("Error Occurred!")
                    return  redirect(url_for('index'))
                cur.close()
                session.clear()
        else:
            flash("Password not match.")
            return render_template('register.html')
            
    return render_template('register.html')




@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        # Process the form data as needed
        return redirect(url_for('index'))
    return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)
