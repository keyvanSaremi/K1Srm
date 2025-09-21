from flask import Flask, render_template, request, redirect, session, flash
from helpers import login_required, hash_password, check_password
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ---------- اتصال به دیتابیس ----------
def get_db_connection():
    conn = sqlite3.connect("shows.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------- initialize db ----------
from db import init_db
init_db()

# ----------------- ROUTES -----------------

@app.route("/")
@login_required
def index():
    conn = get_db_connection()
    shows = conn.execute("SELECT * FROM shows WHERE user_id=?", (session["user_id"],)).fetchall()
    conn.close()
    return render_template("index.html", shows=shows)

# ---------- REGISTER ----------
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        if not username or not password or not confirm:
            flash("All fields are required!")
            return redirect("/register")
        if password != confirm:
            flash("Passwords do not match!")
            return redirect("/register")

        hashed = hash_password(password)
        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hashed))
            conn.commit()
            # لاگین خودکار بعد از ثبت نام
            user_id = conn.execute("SELECT id FROM users WHERE username=?", (username,)).fetchone()["id"]
            session["user_id"] = user_id
            conn.close()
            flash("Registered successfully! Please add your first show.")
            return redirect("/add_show")
        except sqlite3.IntegrityError:
            flash("Username already taken!")
            return redirect("/register")
    return render_template("register.html")

# ---------- LOGIN ----------
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE username=?", (username,)).fetchone()
        conn.close()

        if not user or not check_password(user["hash"], password):
            flash("Invalid username or password!")
            return redirect("/login")

        session["user_id"] = user["id"]
        flash("Logged in successfully!")
        return redirect("/")
    return render_template("login.html")

# ---------- LOGOUT ----------
@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Logged out successfully!")
    return redirect("/login")

# ---------- CHANGE PASSWORD ----------
@app.route("/change_password", methods=["GET","POST"])
@login_required
def change_password():
    if request.method == "POST":
        old = request.form.get("old_password")
        new = request.form.get("new_password")
        confirm = request.form.get("confirm")

        conn = get_db_connection()
        user = conn.execute("SELECT * FROM users WHERE id=?", (session["user_id"],)).fetchone()

        if not check_password(user["hash"], old):
            flash("Old password incorrect!")
            conn.close()
            return redirect("/change_password")
        if new != confirm:
            flash("New passwords do not match!")
            conn.close()
            return redirect("/change_password")

        hashed = hash_password(new)
        conn.execute("UPDATE users SET hash=? WHERE id=?", (hashed, session["user_id"]))
        conn.commit()
        conn.close()
        flash("Password changed successfully!")
        return redirect("/")
    return render_template("change_password.html")

# ---------- ADD SHOW ----------
@app.route("/add_show", methods=["GET","POST"])
@login_required
def add_show():
    if request.method == "POST":
        name = request.form.get("name")
        season = request.form.get("season")
        episode = request.form.get("episode")

        if not name or not season or not episode:
            flash("All fields are required!")
            return redirect("/add_show")

        last_episode = f"S{season} : E{episode}"

        conn = get_db_connection()
        conn.execute("INSERT INTO shows (user_id, name, last_episode) VALUES (?, ?, ?)",
                     (session["user_id"], name, last_episode))
        conn.commit()
        conn.close()
        flash("Show added successfully!")
        return redirect("/")
    return render_template("add_show.html")

# ---------- EDIT SHOW ----------
@app.route("/edit_show/<int:show_id>", methods=["GET","POST"])
@login_required
def edit_show(show_id):
    conn = get_db_connection()
    show = conn.execute("SELECT * FROM shows WHERE id=? AND user_id=?", (show_id, session["user_id"])).fetchone()
    if not show:
        conn.close()
        flash("Show not found!")
        return redirect("/")

    if request.method == "POST":
        name = request.form.get("name")
        season = request.form.get("season")
        episode = request.form.get("episode")
        if not name or not season or not episode:
            flash("All fields are required!")
            return redirect(f"/edit_show/{show_id}")

        last_episode = f"S{season} : E{episode}"

        conn.execute("UPDATE shows SET name=?, last_episode=? WHERE id=? AND user_id=?",
                     (name, last_episode, show_id, session["user_id"]))
        conn.commit()
        conn.close()
        flash("Show updated successfully!")
        return redirect("/")

    # جدا کردن فصل و اپیزود برای فرم
    if "S" in show["last_episode"] and "E" in show["last_episode"]:
        try:
            parts = show["last_episode"].split(" : ")
            season = parts[0].replace("S","")
            episode = parts[1].replace("E","")
        except:
            season = ""
            episode = ""
    else:
        season = ""
        episode = ""

    conn.close()
    return render_template("edit_show.html", show=show, season=season, episode=episode)

# ---------- DELETE SHOW ----------
@app.route("/delete_show/<int:show_id>")
@login_required
def delete_show(show_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM shows WHERE id=? AND user_id=?", (show_id, session["user_id"]))
    conn.commit()
    conn.close()
    flash("Show deleted successfully!")
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
