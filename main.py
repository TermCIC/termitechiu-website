from flask import Flask, redirect, url_for, render_template, request, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__, template_folder='templates')
app.secret_key = "12345678"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/aboutus")
def drchiu():
    return render_template("aboutus.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/publications")
def publications():
    return render_template("publications.html")


@app.route('/sample')
def sample():
    return render_template('sample.html')


@app.route('/sample_wrong')
def sample_wrong():
    return render_template('sample_wrong.html')


@app.route('/register')
def register():
    return render_template('register.html')


class UserNotFoundError(Exception):
    def __init__(self, message):
        self.message = message


class User:
    def __init__(self, Email, Password, UserTitle, Company, City, Address, Phone, Fax, EmailCheck, Role):
        self.Email = Email
        self.Password = Password
        self.UserTitle = UserTitle
        self.Company = Company
        self.City = City
        self.Address = Address
        self.Phone = Phone
        self.Fax = Fax
        self.EmailCheck = EmailCheck
        self.Role = Role

    def save_to_db(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        try:
            cursor.execute(
                'INSERT INTO Users (Email, Password, UserTitle, Company, City, Address, Phone, Fax, EmailCheck, Role) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (self.Email, self.Password, self.UserTitle, self.Company, self.City, self.Address, self.Phone, self.Fax,
                 self.EmailCheck, self.Role))
        except:
            cursor.execute(
                'CREATE TABLE Users (Email TEXT, Password TEXT, UserTitle TEXT, Company TEXT, City TEXT, Address TEXT, Phone TEXT, Fax TEXT, EmailCheck TEXT, Role TEXT)')
            raise UserNotFoundError('The table `Users` did not exist, but it was created. Run the registration again.')
        finally:
            connection.commit()
            connection.close()

    @classmethod
    def find_by_username(cls, Email):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        try:
            data = cursor.execute('SELECT * FROM Users WHERE Email=?', (Email,)).fetchone()
            if data:
                return cls(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9])
        finally:
            connection.close()


@app.route('/record', methods=['POST', 'GET'])
def record():
    if request.method == 'POST':
        Email = request.form['Email']
        Password = request.form['Password']
        UserTitle = request.form['UserTitle']
        Company = request.form['Company']
        City = request.form['City']
        Address = request.form['Address']
        Phone = request.form['Phone']
        Fax = request.form['Fax']
        EmailCheck = 'False'
        Role = 'User'
        try:
            User(Email, generate_password_hash(Password), UserTitle, Company, City, Address, Phone, Fax, EmailCheck,
                 Role).save_to_db()
            msg = "Record successfully added."
        except Exception as e:
            msg = "Error in insert operation."
            return jsonify({'error': e.message}), 500
        finally:
            return render_template("result.html", msg=msg)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        Email = request.form['Email']
        Password = request.form['Password']

        user = User.find_by_username(Email)

        if user and check_password_hash(user.Password, Password):
            msg = "Login success!"
            return render_template("result.html", msg=msg)
        else:
            return redirect(url_for("sample_wrong"))


if __name__ == "__main__":
    app.run()
