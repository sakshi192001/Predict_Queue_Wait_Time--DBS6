from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
#from passlib.hash import sha256_crypt
import pickle
import numpy as np
import gspread
from gspread.models import Worksheet
import datetime
from datetime import datetime
from datetime import date
import calendar
#from cryptography.fernet import Fernet
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
reg_model = pickle.load(open('reg_model.pkl', 'rb'))
#model=pickle.load(open('model.pkl','rb'))
# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pqt13'

# Intialize MySQL
mysql = MySQL(app)
run_with_ngrok(app)
# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests
@app.route('/', methods=['GET', 'POST'])
def index():
    # Output message if something goes wrong...
    return render_template('index.html', msg='')

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM entries WHERE Username = %s AND Password = %s', [username, password])
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['Name'] = account['Name']
            session['Username'] = account['Username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        name = request.form['name']
        email = request.form['email']
        gender = request.form['gender']
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM entries WHERE Username = %s AND Password=%s', [username, password])
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO entries VALUES(%s, %s, %s, %s, %s)', (name, email, gender, username, password))
            mysql.connection.commit()
            msg = 'Successfully registered! Please Sign-In'
            return render_template('login.html', msg=msg)
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

@app.route('/home', methods=['GET', 'POST'])
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['Username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/doctor-availability')
def doctor():
    return render_template('doctor-availability.html')

@app.route('/forgot')
def forgot():
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'question' in request.form and 'Answer' in request.form:
        username = request.form['username']
        question= request.form['question']
        Answer = request.form['Answer']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM entries WHERE Username = %s AND Question=%s AND Answer=%s', [username,question,Answer])
        account = cursor.fetchone()
        if account:
            return render_template('rest_password.html')
        else:
            msg="Account does not exist"
    return render_template('forgot.html',msg=msg)

@app.route('/reset')
def reset():
    return render_template('reset.html')

@app.route('/services-provided')
def services():
    return render_template('services-provided.html')

@app.route('/calculate-wait-time', methods=['GET', 'POST'])
def calculate():
    msg=''
    error=''
    gc = gspread.service_account(filename='credentials.json')
    sh = gc.open_by_key('16WyXcKC7kXRTct7nrSWoUSKJMjoQk4_u7-qbJuqYZL8')
    Worksheet= sh.worksheet('Sheet3')
    list_of_lists = Worksheet.get_all_values()
    my_date = date.today()
    day=calendar.day_name[my_date.weekday()]
    time = datetime.now().strftime("%H:%M:%S")
    hr = time.split(':')[0]
    min = int(time.split(':')[1]) 
    count = 0
    week_number=[]
    for x in list_of_lists:
        if x[2]==day and x[3].split(':')[0]==hr:
            if min <= 15 and min > 0 and int(x[3].split(':')[1])<=15 and int(x[3].split(':')[1])>0:
                count = count+1
                week_number.append(int(x[1]))
            elif min <= 30 and min > 15 and int(x[3].split(':')[1])<=30 and int(x[3].split(':')[1])>15:
                count = count+1
                week_number.append(int(x[1]))
            elif min <= 45 and min > 30 and int(x[3].split(':')[1])<=45 and int(x[3].split(':')[1])>30:
                count = count+1
                week_number.append(int(x[1]))
            elif min <= 60 and min > 45 and int(x[3].split(':')[1])<=60 and int(x[3].split(':')[1])>45:
                count=count+1
                week_number.append(int(x[1]))

    str_reg_time=datetime.now().strftime("%H:%M:%S")
    reg_day = int(datetime.today().weekday())+1
    if str_reg_time > '08:30:00' and str_reg_time <= '9:00:00':
        reg_time=1
    elif str_reg_time > '09:00:00' and str_reg_time <= '09:30:00':
        reg_time=2
    elif str_reg_time > '09:30:00' and str_reg_time <= '10:00:00':
        reg_time=3 
    elif str_reg_time > '10:00:00' and str_reg_time <= '10:30:00':
        reg_time=4 
    elif str_reg_time > '10:30:00' and str_reg_time <= '11:00:00':
        reg_time=5 
    elif str_reg_time > '11:00:00' and str_reg_time <= '11:30:00':
        reg_time=6 
    elif str_reg_time > '11:30:00' and str_reg_time <= '12:00:00':
        reg_time=7 
    elif str_reg_time > '12:00:00' and str_reg_time <= '12:30:00':
        reg_time=8 
    elif str_reg_time > '12:30:00' and str_reg_time <= '13:00:00':
        reg_time=9 
    elif str_reg_time > '13:00:00' and str_reg_time <= '13:30:00':
        reg_time=10 
    elif str_reg_time > '13:30:00' and str_reg_time <= '14:00:00':
        reg_time=11 
    elif str_reg_time > '14:00:00' and str_reg_time <= '14:30:00':
        reg_time=12 
    elif str_reg_time > '14:30:00' and str_reg_time <= '15:00:00':
        reg_time=13
    elif str_reg_time > '15:00:00' and str_reg_time <= '15:30:00':
        reg_time=14
    elif str_reg_time > '15:30:00' and str_reg_time <= '16:00:00':
        reg_time=15 
    elif str_reg_time > '16:00:00' and str_reg_time <= '16:30:00':
        reg_time=16 
    elif str_reg_time > '16:30:00' and str_reg_time <= '17:00:00':
        reg_time=17
    elif str_reg_time > '17:00:00' and str_reg_time <= '17:30:00':
        reg_time=18 
    elif str_reg_time > '17:30:00' and str_reg_time <= '18:00:00':
        reg_time=19 
    elif str_reg_time > '18:00:00' and str_reg_time <= '18:30:00':
        reg_time=20 
    elif str_reg_time > '18:30:00' and str_reg_time <= '19:00:00':
        reg_time=21 
    elif str_reg_time > '19:00:00' and str_reg_time <= '19:30:00':
        reg_time=22 
    elif str_reg_time > '19:30:00' and str_reg_time <= '20:00:00':
        reg_time=23 
    elif str_reg_time > '20:00:00' and str_reg_time <= '20:30:00':
        reg_time=24 
    elif str_reg_time > '20:30:00' and str_reg_time <= '21:00:00':
        reg_time=25 
    elif str_reg_time > '21:00:00' and str_reg_time <= '21:30:00':
        reg_time=26
    
    if len(week_number)==0:
        reg_time_pred=0
    else:
        num_of_patients = count/max(week_number)
         
        time_per_person = reg_model.predict([[reg_day,reg_time]])
        
        reg_time_pred = round(time_per_person[0] * num_of_patients)
        

    if request.method == 'POST' and 'rfid' in request.form:
        str_rfid=request.form['rfid']
        rfid=str_rfid+'\r'
        gc = gspread.service_account(filename='credentials.json')
        sh = gc.open_by_key('16WyXcKC7kXRTct7nrSWoUSKJMjoQk4_u7-qbJuqYZL8')
        Worksheet= sh.worksheet('Sheet3')
        f1 = int(datetime.today().weekday())+1
        f2=datetime.now().strftime("%H:%M:%S")
        list_of_lists=Worksheet.get_all_values()
        count_bill=0
        count_treatment=0
        for x in list_of_lists[::-1]:
            if rfid==x[0]:
                doctor=x[5]
                day=x[2]
                week=x[1]
                time_of_bill=x[15]
                index=list_of_lists.index(x)
                for y in range(0,index):
                    if doctor==list_of_lists[y][5] and day==list_of_lists[y][2] and week==list_of_lists[y][1] and str(time_of_bill)>str(list_of_lists[y][15]):
                        count_bill=count_bill+1
                        if str(time_of_bill)<str(list_of_lists[y][16]):
                            count_treatment=count_treatment+1        
        pts_ahead_in_q= count_bill-count_treatment
        f4=pts_ahead_in_q  
        for x in list_of_lists[::-1]:
            if rfid==x[0]:
                f3=x[5]
                if f3== "A":
                    f33=1
                elif f3 == "B":
                    f33=2
                elif f3 == "C":
                    f33=3
                elif f3 == "D":
                    f33=4
                elif f3 == "E":
                    f33=5
                elif f3 == "F":
                    f33=6
                elif f3 == "G":
                    f33=7
                elif f3 == "H":
                    f33=8
                elif f3 == "I":
                    f33=9
                elif f3 == "J":
                    f33=10
                elif f3 == "K":
                    f33=11
                elif f3=="L":
                    f33=12                

        if f2 >= "8:00:00" and f2<="09:00:00":
            f22 = 1 
        elif f2 >= "09:00:00" and f2<="10:00:00":
            f22 = 2
        elif f2 >= "11:00:00" and f2<="12:00:00":
            f22 = 3
        elif f2 >= "12:00:00" and f2<="13:00:00":
            f22 = 4
        elif f2 >= "13:00:00" and f2<="14:00:00":
            f22 = 5
        elif f2 >= "14:00:00" and f2<="15:00:00":
            f22 = 6
        elif f2 >= "15:00:00" and f2<="16:00:00":
            f22 = 7
        elif f2 >= "16:00:00" and f2<="17:00:00":
            f22 = 8
        elif f2 >= "17:00:00" and f2<="18:00:00":
            f22 = 9
        elif f2 >= "18:00:00" and f2<="19:00:00":
            f22 = 10
        elif f2 >= "19:00:00" and f2<="20:00:00":
            f22 = 11
        elif f2 >= "20:00:00" and f2<="21:00:00":
            f22 = 12
        elif f2 >= "21:00:00" and f2<="22:00:00":
            f22 = 13
        elif f2 >= "22:00:00" and f2<="23:00:00":
            f22 = 14
        else:
            f22 = 15
        
        
        msgs = model.predict([[f1,f22,f33,f4]])
        print(f1,f22,f33,f4)
        for x in msgs:
            return render_template('prediction.html',msg=int(x),pts=pts_ahead_in_q)

    return render_template('calculate-wait-time.html',msg=reg_time_pred,error=error)

@app.errorhandler(UnboundLocalError)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html')
    
@app.route('/prediciton')
def calculated():
    return render_template('calculated-wait-time.html')

@app.route('/planning-a-visit', methods=['GET', 'POST'])
def planningavisit():
    msg=''
    if request.method == 'POST' and 'day' in request.form and 'doctor' in request.form and 'time' in request.form:
        day = request.form.get('day')
        time = str(request.form.get('time'))
        doctor = request.form.get('doctor')
        gc = gspread.service_account(filename='credentials.json')
        sh = gc.open_by_key('16WyXcKC7kXRTct7nrSWoUSKJMjoQk4_u7-qbJuqYZL8')
        Worksheet= sh.worksheet('Sheet3')
        list_of_lists = Worksheet.get_all_values()
        hr = time.split(':')[0]
        nxt_hr = int(hr)+1
        prev_hr = int(hr)
        global list_of_total_time
        list_of_total_time = []
        for x in list_of_lists:
            if x[2]==day and x[5]==doctor and x[18]<str(date.today()):
                if time > '08:00:00' and time <= '10:00:00' and x[3]> '08:00:00' and x[3]<='10:00:00':
                    list_of_total_time.append(x[14])
                elif time > '10:00:00' and time <= '11:00:00' and x[3]> '10:00:00' and x[3]<='11:00:00':
                    list_of_total_time.append(x[14])
                elif time > '11:00:00' and time <= '12:00:00' and x[3]> '11:00:00' and x[3]<='12:00:00':
                    list_of_total_time.append(x[14])
                elif time > '12:00:00' and time <= '13:00:00' and x[3]> '12:00:00' and x[3]<='13:00:00':
                    list_of_total_time.append(x[14])
                elif time > '13:00:00' and time <= '14:00:00' and x[3]> '13:00:00' and x[3]<='14:00:00':
                    list_of_total_time.append(x[14])
                elif time > '14:00:00' and time <= '15:00:00' and x[3]> '14:00:00' and x[3]<='15:00:00':
                    list_of_total_time.append(x[14])
                elif time > '15:00:00' and time <= '16:00:00' and x[3]> '15:00:00' and x[3]<='16:00:00':
                    list_of_total_time.append(x[14])
                elif time > '16:00:00' and time <= '17:00:00' and x[3]> '16:00:00' and x[3]<='17:00:00':
                    list_of_total_time.append(x[14])
                elif time > '17:00:00' and time <= '18:00:00' and x[3]> '17:00:00' and x[3]<='18:00:00':
                    list_of_total_time.append(x[14])
                elif time > '18:00:00' and time <= '19:00:00' and x[3]> '18:00:00' and x[3]<='19:00:00':
                    list_of_total_time.append(x[14])
                elif time > '19:00:00' and time <= '20:00:00' and x[3]> '19:00:00' and x[3]<='20:00:00':
                    list_of_total_time.append(x[14])
        return render_template('registration-wait-time.html',msg=average())
    return render_template('planning-a-visit.html',msg=msg)
def average():
    total=0
    counter=0
    for i in list_of_total_time:
        total=total+int(i)
        counter = counter+1
    if counter == 0:
        avg= "You have entered invalid details. Kindly check doctor's availability."
    else:  
        avg="Your expected total journey time will be "+str(int(total/counter))+ " minutes approximately."
    return avg
@app.route('/registration-wait-time')
def registrationwaittime():
    return render_template('registration-wait-time.html')

@app.route('/tp')
def tp():
    return render_template('tp.html')

if __name__ == '__main__':
    app.run()