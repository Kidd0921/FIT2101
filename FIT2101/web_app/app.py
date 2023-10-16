from flask import Flask, redirect, url_for, render_template, request, session
from datetime import date, datetime

import pyrebase

# configuration to bind firebase to the application using pyrebase
config = {
    "apiKey": "AIzaSyCKd98J2YGEqTo-sgFxHH5VjX1Q58RySM0",
    "authDomain": "fit2101-ef857.firebaseapp.com",
    "databaseURL": "https://fit2101-ef857-default-rtdb.firebaseio.com/",
    "projectId": "fit2101-ef857",
    "storageBucket": "fit2101-ef857.appspot.com",
    "messagingSenderId": "905296140772",
    "appId": "1:905296140772:web:cce989337ad087cb4c0ff1",
    "measurementId": "G-NWSRNK0YMB"
}

# initializing the database in order to use it for the application
firebase = pyrebase.initialize_app(config)
db = firebase.database()
# handles authentication for the website
auth = firebase.auth()
app = Flask(__name__)
app.secret_key = "assignment"

# home page for users. allows for their name to be shown on the homepage.


@app.route('/', methods=['GET', 'POST'])
def home():
    if "user" in session:
        user = session["user"]
        username = db.child('user').child(
            user[:user.index('@')]).child('username').get().val()
        user = session["user"]
        email = db.child('user').child(
            user[:user.index('@')]).child('email').get().val()
        user = session["user"]
        number = db.child('user').child(
            user[:user.index('@')]).child('number').get().val()
        user = session["user"]
        profile = db.child('user').child(
            user[:user.index('@')]).child('profile').get().val()
        user = session["user"]
        superUser = db.child('user').child(
            user[:user.index('@')]).child('superUser').get().val()
        user = user[:user.index('@')]
        data = [get_total_local(), get_total_sg(),
                get_total_uk(), get_total_us()]
        label = ['Malaysia', 'Singapore', 'United Kingdom', 'United States']
        vaccine_label = ['Pfizer', 'Sinovac', 'Astrazeneca']
        global_vaccine_label = get_global_vaccine_label()
        global_vaccine_amount = get_global_vaccine_amount()
        daily_label = get_date_local()
        daily_case = get_daily_local()
        daily_recovered = get_daily_recovered_local()
        vaccine_data = [get_pfizer_vaccinated_local(
        ), get_sinovac_vaccinated_local(), get_az_vaccinated_local()]
        total_vaccine_local = get_total_vaccine_local()
        return render_template("home.html", loggedIn=True, superUser=superUser, user=user, data=data, username=username, email=email, number=number, profile=profile, label=label, vaccine_data=vaccine_data, daily_case=daily_case, daily_label=daily_label, vaccine_label=vaccine_label, daily_recovered=daily_recovered, global_vaccine_label=global_vaccine_label, global_vaccine_amount=global_vaccine_amount, total_vaccine_local=total_vaccine_local)
    else:
        return redirect(url_for('login', loggedIn=False))

# signup page for the users, valid signUps will be handled by the firebase authentication system


@app.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        email = request.form['email']    # gets email from html field
        password = request.form['pass']  # gets password from html field
        # makes sure password is the same
        pass_confirmation = request.form['pass_confirm']
        number = request.form['number']  # gets password from html field
        profile = request.form['profile']  # gets password from html field
        username = request.form['username']  # gets password from html field
        if(request.form.getlist('check')) == []:
            superuser = False
        else:
            superuser = True
        if password != pass_confirmation:
            return 'Please enter the same password'
        else:
            try:
                # creates user using the email and password taken from the fields
                auth.create_user_with_email_and_password(email, password)
            except:
                return render_template('signUp.html', us='Please enter valid email or password', loggedIn=False)
            else:
                node = db.child('user/'+email[:email.index('@')])
                node.set({
                    "email": email,
                    "username": username,
                    "profile": profile,
                    "number": number,
                    "created": str(date.today()),
                    "last_signed_in": str(date.today()),
                    "counter": 0,
                    "superUser": superuser
                })
                return redirect(url_for('login', loggedIn=False))
    return render_template('signUp.html', loggedIn=False)

# login page for the users, when user enters invalid password or email, they will be returned to the login page.


@app.route('/login', methods=['GET', 'POST'])
def login():

    if "user" in session:
        return redirect(url_for('home',  loggedIn=True))
    else:

        if request.method == 'POST':
            email = request.form['email']    # gets email from html field
            password = request.form['pass']  # gets password from html field
            try:
                auth.sign_in_with_email_and_password(email, password)
                # Creates a new session once successfully logged in
                session["user"] = email
            except:
                return render_template('login.html', us='Please enter valid email or password')
            else:
                counter = db.child(
                    'user/'+email[:email.index('@')]+'/counter').get().val()

                db.child('user/'+email[:email.index('@')]
                         ).update({'counter': counter+1})
                db.child('user/'+email[:email.index('@')]
                         ).update({"last_signed_in": str(date.today())})

                return redirect(url_for('home', loggedIn=True))

    return render_template('login.html', loggedIn=False)

# database method to handle adding the amount of cases into the firebase.


@app.route('/database', methods=['GET', 'POST'])
def database():
    if "user" not in session:
        return redirect(url_for('login', loggedIn=False))
    if request.method == 'POST':
        # creates a object with the information and adds it into the firebase
        user = session["user"]
        user = user[:user.index('@')]
        cases = request.form['newCases']
        importCases = request.form['importCases']
        recoveredCases = request.form['recoveredCases']
        today = str(date.today())
        day = date.today() - date(2020, 1, 25)
        node = db.child(str(day)[:3])
        node.set({
            "cases_new": cases,
            "cases_import": importCases,
            "cases_recovered": recoveredCases,
            "date": str(today)
        })
    return render_template('database.html', loggedIn=True, user=user)

# dummy sites for features that are to be implemented during sprint 2.


@app.route('/confirmedCases')
def confirmedCases():
    return render_template('coronaCases.html', loggedIn=True)


@app.route('/vaccinated')
def vaccinated():
    return render_template('vaccinated.html', loggedIn=True)


@app.route('/history')
def history():
    return render_template('history.html', loggedIn=True)


@app.route('/admin')
def admin():
    user = session["user"]
    username = db.child('user').child(
        user[:user.index('@')]).child('username').get().val()
    user = session["user"]
    email = db.child('user').child(
        user[:user.index('@')]).child('email').get().val()
    user = session["user"]
    number = db.child('user').child(
        user[:user.index('@')]).child('number').get().val()
    user = session["user"]
    profile = db.child('user').child(
        user[:user.index('@')]).child('profile').get().val()
    user = user[:user.index('@')]
    return render_template('admin.html', loggedIn=True, user=user, username=username, email=email, number=number, profile=profile)

    # return render_template('admin.html', loggedIn=True)

# ends the current session


@app.route('/logout')
def logout():
    if "user" in session:
        session.pop("user", None)
    return redirect(url_for('home', loggedIn=False))


def get_daily_local():
    data = db.child("local").get()
    array = []
    for data in data.each():
        array.append((data.val()['cases_new']))
    return array


def get_daily_recovered_local():
    data = db.child("local").get()
    array = []
    for data in data.each():
        array.append((data.val()['cases_recovered']))
    return array


def get_date_local():
    data = db.child("local").get()
    array = []
    for data in data.each():
        array.append((data.val()['date']))
    return array


def get_total_local():
    data = db.child("local").get()
    total = 0
    for data in data.each():
        total += (data.val()['cases_new'])
    return total


def get_total_sg():
    data = db.child("sg").get()
    total = 0
    for data in data.each():
        if (data.val()['B']) != "Daily Confirmed" and (data.val()['B']) != "":
            total += int((data.val()['B']))
    return total


def get_pfizer_vaccinated_local():
    data = db.child("local_vac").get()
    return((data.val()[0]['doses']))


def get_sinovac_vaccinated_local():
    data = db.child("local_vac").get()
    return((data.val()[1]['doses']))


def get_az_vaccinated_local():
    data = db.child("local_vac").get()
    return((data.val()[2]['doses']))


def get_global_vaccine_label():
    data = db.child("global_vac").get()
    total_vaccine = []
    for data in data.each():
        current_vaccine = (data.val()['vaccines'].replace(' ', '').split(','))
        for x in current_vaccine:
            if x not in total_vaccine:
                total_vaccine.append(x)
    return(total_vaccine)


def get_global_vaccine_amount():
    data = db.child("global_vac").get()
    size = len(get_global_vaccine_label())
    vaccine_label = get_global_vaccine_label()
    count_array = [None] * (size)
    # avoid list reference error
    for i in range(len(count_array)):
        count_array[i] = 0
    current_vaccine = []
    for data in data.each():
        current_vaccine.append(
            data.val()['vaccines'].replace(' ', '').split(','))
    for x in range(len(current_vaccine)):
        for y in range(len(current_vaccine[x])):
            for z in range(len(vaccine_label)):
                if current_vaccine[x][y] == vaccine_label[z]:
                    count_array[z] += 1
    return(count_array)


def get_total_uk():
    data = db.child("uk").get()
    total = 0
    for data in data.each():
        total += (data.val()['newCasesByPublishDate'])
    return total


def get_total_us():
    data = db.child("us").get()
    total = 0
    for data in data.each():
        total += (data.val()['positiveIncrease'])
    return total


def get_total_vaccine_local():
    total = get_az_vaccinated_local() + get_pfizer_vaccinated_local() + \
        get_sinovac_vaccinated_local()
    total_str = "{:,}".format(total)
    return total_str


if __name__ == "main":
    app.run(debug=True)
