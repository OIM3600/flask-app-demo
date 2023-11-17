from flask import Flask, redirect, render_template, request, g
import sqlite3

app = Flask(__name__)

# 1. Configuration settings
app.config["TEMPLATES_AUTO_RELOAD"] = True
DATABASE = "database.db"


# 2. Database initialization
def create_table():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """
        )
        db.commit()


def get_db():
    if not hasattr(g, "db"):
        g.db = sqlite3.connect(DATABASE)
    return g.db


@app.before_first_request
def before_first_request():
    create_table()


# 3. Request handling
@app.before_request
def before_request():
    g.db = sqlite3.connect(DATABASE)


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, "db"):
        g.db.close()


# 4. Route definitions
@app.route("/")
def index():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template("index.html", users=users)


@app.post("/add")
def add_user():
    name = request.form.get("name")
    email = request.form.get("email")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, email) VALUES (?, ?);", (name, email))
    db.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
