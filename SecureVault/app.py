# from flask import Flask, render_template, request

# app = Flask(__name__)

# @app.route("/")
# def home():
#     return "SecureVault is running!"

# @app.route("/login", methods=["GET", "POST"])
# def login():
    
#     if request.method == "POST":
        
#         username = request.form["username"]
#         password = request.form["password"]

#         print("Username:", username)
#         print("Password:", password)

#         return "Login data received!"

#     return render_template("login.html")


# if __name__ == "__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = "supersecretkey"


@app.route("/")
def home():
    return "SecureVault is running!"

# @app.route("/register", methods=["GET", "POST"])
# def register():

#     if request.method == "POST":

#         username = request.form["username"]
#         password = request.form["password"]

#         conn = sqlite3.connect("users.db")
#         cursor = conn.cursor()

#         cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
#                        (username, password))

#         conn.commit()
#         conn.close()

#         return "User registered successfully!"

#     return render_template("register.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # HASH PASSWORD
        hashed_password = generate_password_hash(password)

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, hashed_password)
        )

        conn.commit()
        conn.close()

        return "User registered successfully!"

    return render_template("register.html")



# @app.route("/login", methods=["GET", "POST"])
# def login():

#     if request.method == "POST":

#         username = request.form["username"]
#         password = request.form["password"]

#         print(username, password)

#         return "Login data received!"

#     return render_template("login.html")
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        # connect to database
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        # check user
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        result = cursor.fetchone()

        conn.close()

        # if user:
        #     return "Login successful!"
        # if user:
        #     return render_template("dashboard.html")
        # if result and check_password_hash(result[0], password):
        #     return render_template("dashboard.html")
        if result and check_password_hash(result[0], password):

            # CREATE SESSION
            session["username"] = username
            return redirect("/dashboard")
        else:
            return "Invalid username or password!"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "username" in session:
        return render_template("dashboard.html")

    return redirect("/login")

@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect("/login")



if __name__ == "__main__":
    app.run(debug=True)


