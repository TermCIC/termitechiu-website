from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import ujson as json
from datetime import datetime
import uuid
import urllib3
from bs4 import BeautifulSoup

geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?"
app = Flask(__name__, template_folder='templates')
app.secret_key = "12345678"
app.config['GOOGLEMAPS_KEY'] = ""

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": '',
    "MAIL_PASSWORD": ''
}

app.config.update(mail_settings)
mail = Mail(app)

s = URLSafeTimedSerializer('Thisisasecret!')


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/member")
def member():
    if "User" in session:
        user_name = session["User"]
        user_email = session["Email"]
        with open('./Users.json', 'r') as file:
            Users = json.load(file)
            file.close()
        user_company = Users[str(user_email)]["Company"]
        user_province = Users[str(user_email)]["Province"]
        user_city = Users[str(user_email)]["City"]
        user_address = Users[str(user_email)]["Address"]
        user_phone = Users[str(user_email)]["Phone"]
        user_fax = Users[str(user_email)]["Fax"]
        collection = Users[str(user_email)]["Collection"]
        user_collection = str(len(collection))

        return render_template("member.html",
                               user_name=user_name,
                               user_email=user_email,
                               user_company=user_company,
                               user_province=user_province,
                               user_city=user_city,
                               user_address=user_address,
                               user_phone=user_phone,
                               user_fax=user_fax,
                               user_collection=user_collection
                               )
    else:
        return redirect(url_for("login"))


@app.route("/edit", methods=['POST', 'GET'])
def edit():
    if request.method == 'POST':
        user_name = session["User"]
        user_email = session["Email"]
        UserTitle = request.form['Name']
        Company = request.form['Company']
        Province = request.form['Province']
        City = request.form['City']
        Address = request.form['Address']
        Phone = request.form['Phone']
        Fax = request.form['Fax']
        with open('./Users.json', 'r') as file:
            Users = json.load(file)
            file.close()
        Users[str(user_email)]["UserTitle"] = UserTitle
        Users[str(user_email)]["Company"] = Company
        Users[str(user_email)]["Province"] = Province
        Users[str(user_email)]["City"] = City
        Users[str(user_email)]["Address"] = Address
        Users[str(user_email)]["Phone"] = Phone
        Users[str(user_email)]["Fax"] = Fax
        with open('./Users.json', 'w') as file:
            json.dump(Users, file)

        user_company = Users[str(user_email)]["Company"]
        user_province = Users[str(user_email)]["Province"]
        user_city = Users[str(user_email)]["City"]
        user_address = Users[str(user_email)]["Address"]
        user_phone = Users[str(user_email)]["Phone"]
        user_fax = Users[str(user_email)]["Fax"]
        collection = Users[str(user_email)]["Collection"]
        user_collection = str(len(collection))
        return render_template("member.html",
                               user_name=user_name,
                               user_email=user_email,
                               user_company=user_company,
                               user_province=user_province,
                               user_city=user_city,
                               user_address=user_address,
                               user_phone=user_phone,
                               user_fax=user_fax,
                               user_collection=user_collection
                               )

    if "User" in session:
        user_name = session["User"]
        user_email = session["Email"]
        with open('./Users.json', 'r') as file:
            Users = json.load(file)
            file.close()
        user_company = Users[str(user_email)]["Company"]
        user_province = Users[str(user_email)]["Province"]
        user_city = Users[str(user_email)]["City"]
        user_address = Users[str(user_email)]["Address"]
        user_phone = Users[str(user_email)]["Phone"]
        user_fax = Users[str(user_email)]["Fax"]
        collection = Users[str(user_email)]["Collection"]
        user_collection = str(len(collection))
        return render_template("edit.html",
                               user_name=user_name,
                               user_email=user_email,
                               user_company=user_company,
                               user_province=user_province,
                               user_city=user_city,
                               user_address=user_address,
                               user_phone=user_phone,
                               user_fax=user_fax,
                               user_collection=user_collection)
    else:
        return redirect(url_for("login"))


@app.route("/sample")
def sample():
    if "User" in session:
        with open('./Users.json', 'r') as file:
            Users = json.load(file)
            file.close()
        user_name = session["User"]
        user_email = session["Email"]
        user_company = Users[str(user_email)]["Company"]
        user_province = Users[str(user_email)]["Province"]
        user_city = Users[str(user_email)]["City"]
        user_address = Users[str(user_email)]["Address"]
        user_phone = Users[str(user_email)]["Phone"]
        user_fax = Users[str(user_email)]["Fax"]
        collection = Users[str(user_email)]["Collection"]
        user_collection = str(len(collection))
        current_year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        return render_template("sample.html",
                               collection_latitude="15.8700",
                               collection_longitude="100.9925",
                               collection_habitat="Please select...",
                               current_year=current_year,
                               collection_year=current_year,
                               collection_month=month,
                               collection_day=day,
                               collector=user_name,
                               user_email=user_email,
                               user_company=user_company,
                               collection_province=user_province,
                               collection_city=user_city,
                               collection_address=user_address,
                               user_phone=user_phone,
                               user_fax=user_fax,
                               user_collection=user_collection
                               )
    else:
        return redirect(url_for("login"))


@app.route("/submit_sample", methods=['POST', 'GET'])
def submit_sample():
    if "User" in session:
        with open('./Users.json', 'r') as file:
            Users = json.load(file)
            file.close()
        user_name = session["User"]
        user_email = session["Email"]
        user_company = Users[str(user_email)]["Company"]
        user_province = Users[str(user_email)]["Province"]
        user_city = Users[str(user_email)]["City"]
        user_address = Users[str(user_email)]["Address"]
        user_phone = Users[str(user_email)]["Phone"]
        user_fax = Users[str(user_email)]["Fax"]
        collection = Users[str(user_email)]["Collection"]
        user_collection = str(len(collection))

        if request.method == 'POST':
            collector = request.form['collector']
            habitat = request.form['habitat']
            year = request.form['year']
            month = request.form['month']
            day = request.form['date']
            province = request.form['province']
            city = request.form['city']
            address = request.form['address']
            current_year = datetime.now().year
            if request.form['submit_button'] == "Submit":
                hash = uuid.uuid4().hex
                time_stamp = str(datetime.now())[:10].replace("-", "") + str(user_email[:5]) + "_" + str(hash[:5])
                Users[user_email]["Collection"][time_stamp] = {}
                Users[user_email]["Collection"][time_stamp]["Time Stamp"] = time_stamp
                Users[user_email]["Collection"][time_stamp]["Collector"] = collector
                Users[user_email]["Collection"][time_stamp]["Habitat"] = habitat
                Users[user_email]["Collection"][time_stamp]["Year"] = year
                Users[user_email]["Collection"][time_stamp]["Month"] = month
                Users[user_email]["Collection"][time_stamp]["Date"] = day
                Users[user_email]["Collection"][time_stamp]["Province"] = province
                Users[user_email]["Collection"][time_stamp]["City"] = city
                Users[user_email]["Collection"][time_stamp]["Address"] = address
                Users[user_email]["Collection"][time_stamp]["Longitude"] = ""
                Users[user_email]["Collection"][time_stamp]["Latitude"] = ""
                Users[user_email]["Collection"][time_stamp]["Identification"] = False
                Users[user_email]["Collection"][time_stamp]["Payment"] = False
                Users[user_email]["Collection"][time_stamp]["Order"] = "Unknown"
                Users[user_email]["Collection"][time_stamp]["Family"] = "Unknown"
                Users[user_email]["Collection"][time_stamp]["Subfamily"] = "Unknown"
                Users[user_email]["Collection"][time_stamp]["Genus"] = "Unknown"
                Users[user_email]["Collection"][time_stamp]["Species"] = "Unknown"

                with open('./Users.json', 'w') as file:
                    json.dump(Users, file)

                return render_template("member.html",
                                       user_name=user_name,
                                       user_email=user_email,
                                       user_company=user_company,
                                       user_province=user_province,
                                       user_city=user_city,
                                       user_address=user_address,
                                       user_phone=user_phone,
                                       user_fax=user_fax,
                                       user_collection=user_collection
                                       )
            elif request.form['submit_button'] == "Check Location":
                collector = request.form['collector']
                habitat = request.form['habitat']
                year = request.form['year']
                month = request.form['month']
                day = request.form['date']
                province = request.form['province']
                city = request.form['city']
                address = request.form['address']
                current_year = datetime.now().year
                addr = "address=" + address + "+" + city + "+" + province
                addr = addr.replace(" ", "+")
                key = "&key=AIzaSyDkD4Oow18t53T8SPRB7SFsBcwWTaHfF6I"
                url = geocode_url + addr + key
                http = urllib3.PoolManager()
                response = http.request('GET', url)
                geocode = BeautifulSoup(response.data, features="html.parser")
                geocode = json.loads(geocode.text)
                location = dict(geocode.get("results")[0].get("geometry").get("location"))
                latitude = location['lat']
                longitude = location['lng']
                return render_template("sample.html",
                                       collection_latitude=latitude,
                                       collection_longitude=longitude,
                                       collection_habitat=habitat,
                                       current_year=current_year,
                                       collection_year=year,
                                       collection_month=month,
                                       collection_day=day,
                                       collector=collector,
                                       user_email=user_email,
                                       user_company=user_company,
                                       collection_province=province,
                                       collection_city=city,
                                       collection_address=address,
                                       user_phone=user_phone,
                                       user_fax=user_fax,
                                       user_collection=user_collection
                                       )
    else:
        return render_template("login.html")


@app.route("/collection")
def collection():
    if "User" in session:
        user_name = session["User"]
        user_email = session["Email"]
        with open('./Users.json', 'r') as file:
            Users = json.load(file)
            file.close()
        collection = Users[user_email]["Collection"]
        if len(collection) != 0:
            headings = ["Time Stamp", "Collector", "Habitat", "Year", "Month", "Date", "City", "Address", "Payment",
                        "Order", "Family", "Genus", "Species"]
            data = []
            for i in collection:
                row = []
                for j in headings:
                    row.append(collection[i][j])
                data.append(row)
        else:
            log = "You have no termite collection."
        return render_template("collection.html",
                               user_name=user_name,
                               headings=headings,
                               data=data)
    else:
        return redirect(url_for("login"))


@app.route('/login_wrong')
def member_login_wrong():
    return render_template('login_wrong.html')


@app.route('/register')
def register():
    return render_template('register.html')


class UserNotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class User:
    def __init__(self, Email, Password, UserTitle, Company, Province, City, Address, Phone, Fax):
        self.Email = Email
        self.Password = Password
        self.UserTitle = UserTitle
        self.Company = Company
        self.Province = Province
        self.City = City
        self.Address = Address
        self.Phone = Phone
        self.Fax = Fax
        self.EmailCheck = False
        self.Role = "User"
        self.Collection = {}

    def add_user(self):
        with open('./Users.json', 'r') as file:
            Users = json.load(file)
            file.close()
        Users[str(self.Email)] = {}
        Users[str(self.Email)]["Email"] = str(self.Email)
        Users[str(self.Email)]["Password"] = str(self.Password)
        Users[str(self.Email)]["UserTitle"] = str(self.UserTitle)
        Users[str(self.Email)]["Company"] = str(self.Company)
        Users[str(self.Email)]["Province"] = str(self.Province)
        Users[str(self.Email)]["City"] = str(self.City)
        Users[str(self.Email)]["Address"] = str(self.Address)
        Users[str(self.Email)]["Phone"] = str(self.Phone)
        Users[str(self.Email)]["Fax"] = str(self.Fax)
        Users[str(self.Email)]["EmailCheck"] = str(self.EmailCheck)
        Users[str(self.Email)]["Role"] = str(self.Role)
        Users[str(self.Email)]["Collection"] = self.Collection
        with open('./Users.json', 'w') as file:
            json.dump(Users, file)

    @classmethod
    def find_by_username(cls, Email):
        with open('./Users.json', 'r') as file:
            Users = json.load(file)
            file.close()
        user = Users.get(str(Email))
        return user


@app.route('/record', methods=['POST', 'GET'])
def record():
    if request.method == 'POST':
        Email = request.form['Email']
        Password = request.form['Password']
        UserTitle = request.form['UserTitle']
        Company = request.form['Company']
        Province = request.form['Province']
        City = request.form['City']
        Address = request.form['Address']
        Phone = request.form['Phone']
        Fax = request.form['Fax']

        if User.find_by_username(str(Email)) != None:
            msg = "E-mail address is duplicated."
            return render_template("result.html", msg=msg)
        else:
            User(Email, generate_password_hash(Password), UserTitle, Company, Province, City, Address, Phone,
                 Fax).add_user()
            msg = "You successfully registered your account."
            msg += "\n" + "We have sent a confirmation link to your E-mail address: " + str(Email)
            token = s.dumps(Email, salt='email-confirm')
            letter = Message('Confirm Email', sender='tim77918@gmail.com', recipients=[Email])
            link = url_for('confirm_email', token=token, external=True)
            link = "http://127.0.0.1:5000" + link
            letter.body = 'Your link is {}'.format(link)
            mail.send(letter)
            return render_template("result.html", msg=msg)


@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        if email:
            with open('./Users.json', 'r') as file:
                Users = json.load(file)
                file.close()
            Users[str(email)]["EmailCheck"] = True
            with open('./Users.json', 'w') as file:
                json.dump(Users, file)

    except SignatureExpired:
        msg = 'The confirmation token of your E-mail address is expired!'
        return render_template("result.html", msg=msg)
    msg = 'Your E-mail address is confirmed!'
    return render_template("result.html", msg=msg)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        Email = request.form['Email']
        Password = request.form['Password']
        user = User.find_by_username(Email)
        if user:
            with open('./Users.json', 'r') as file:
                Users = json.load(file)
                file.close()
            user_password = Users[str(Email)]["Password"]
            user_name = Users[str(Email)]["UserTitle"]
            user_email = Users[str(Email)]["Email"]
            if check_password_hash(user_password, Password):
                session["Email"] = user_email
                session["User"] = user_name
                return redirect(url_for("member"))
            else:
                return render_template("login_wrong.html", msg="Email and password mismatch!")
        else:
            return render_template("login_wrong.html", msg="User not exist!")

    else:
        if "User" in session:
            return redirect(url_for("member"))

        return render_template("login.html")


@app.route('/logout')
def logout():
    session.pop("User", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()
