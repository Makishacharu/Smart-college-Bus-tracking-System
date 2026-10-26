from ai_eta import model
from flask import Flask, request, redirect, session, jsonify, render_template_string
import sqlite3
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)

app.secret_key = "college_bus_secret_key_2026"

DB_PATH = "database/college_bus.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# =========================================================
# DATABASE INITIALIZATION
# =========================================================

def init_database():

    os.makedirs("database", exist_ok=True)

    connection = get_connection()
    cursor = connection.cursor()

    # STUDENTS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INTEGER PRIMARY KEY AUTOINCREMENT,
            college_id INTEGER UNIQUE,
            name TEXT NOT NULL,
            roll_number TEXT UNIQUE NOT NULL,
            bus_id INTEGER,
            parent_name TEXT,
            parent_phone TEXT
        )
    """)

    # BUSES
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS buses (
            bus_id INTEGER PRIMARY KEY AUTOINCREMENT,
            bus_number TEXT NOT NULL,
            driver_name TEXT NOT NULL,
            route TEXT NOT NULL
        )
    """)

    # ATTENDANCE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY(student_id)
            REFERENCES students(student_id)
        )
    """)

    # NOTIFICATIONS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            notification_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            notification_type TEXT DEFAULT 'Parent',
            created_at TEXT NOT NULL,
            status TEXT DEFAULT 'Queued',
            FOREIGN KEY(student_id)
            REFERENCES students(student_id)
        )
    """)

    connection.commit()
    connection.close()


# =========================================================
# LOGIN REQUIRED
# =========================================================

def login_required(role=None):

    def decorator(function):

        @wraps(function)
        def wrapper(*args, **kwargs):

            if "user_role" not in session:
                return redirect("/login")

            if role and session["user_role"] != role:
                return redirect("/login")

            return function(*args, **kwargs)

        return wrapper

    return decorator


# =========================================================
# COMMON HTML STYLE
# =========================================================

STYLE = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: 'Inter', Arial, sans-serif;
    background:
        radial-gradient(circle at top left, #172554 0%, transparent 35%),
        radial-gradient(circle at bottom right, #312e81 0%, transparent 30%),
        #020617;
    color: #e2e8f0;
    min-height: 100vh;
}


/* ================= NAVBAR ================= */

.navbar {
    background: rgba(15, 23, 42, 0.88);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);

    border-bottom: 1px solid rgba(148,163,184,0.15);

    color: white;
    padding: 18px 32px;

    display: flex;
    justify-content: space-between;
    align-items: center;

    position: sticky;
    top: 0;
    z-index: 1000;

    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}

.navbar h2 {
    margin: 0;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.navbar a {
    color: #cbd5e1;
    text-decoration: none;
    margin-left: 18px;
    font-size: 14px;
    font-weight: 600;

    transition: 0.25s;
}

.navbar a:hover {
    color: #60a5fa;
}


/* ================= CONTAINER ================= */

.container {
    width: 92%;
    max-width: 1250px;
    margin: 35px auto;
}


/* ================= HEADINGS ================= */

h1 {
    font-size: 34px;
    font-weight: 800;
    color: #f8fafc;
    margin-bottom: 10px;
}

h2 {
    color: #f8fafc;
}

h3 {
    color: #e2e8f0;
}


/* ================= CARDS ================= */

.card-container {
    display: grid;
    grid-template-columns:
        repeat(auto-fit, minmax(230px, 1fr));

    gap: 22px;
}

.card {
    background:
        linear-gradient(
            145deg,
            rgba(30,41,59,0.95),
            rgba(15,23,42,0.88)
        );

    border: 1px solid rgba(148,163,184,0.14);

    padding: 26px;

    border-radius: 20px;

    box-shadow:
        0 15px 40px rgba(0,0,0,0.25),
        inset 0 1px 0 rgba(255,255,255,0.04);

    transition:
        transform 0.25s ease,
        box-shadow 0.25s ease,
        border 0.25s ease;
}

.card:hover {
    transform: translateY(-5px);

    border-color: rgba(96,165,250,0.45);

    box-shadow:
        0 20px 50px rgba(0,0,0,0.35),
        0 0 25px rgba(59,130,246,0.08);
}

.card h3 {
    margin-top: 0;
}


/* ================= STAT NUMBERS ================= */

.stat {
    font-size: 38px;
    font-weight: 800;

    background:
        linear-gradient(
            90deg,
            #60a5fa,
            #a78bfa
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-top: 10px;
}


/* ================= BUTTONS ================= */

.btn {
    display: inline-block;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #7c3aed
        );

    color: white;

    padding: 11px 19px;

    border-radius: 10px;

    text-decoration: none;

    border: none;

    cursor: pointer;

    margin: 5px;

    font-weight: 600;
    font-size: 14px;

    box-shadow:
        0 8px 20px rgba(37,99,235,0.25);

    transition: 0.25s;
}

.btn:hover {
    transform: translateY(-2px);

    box-shadow:
        0 12px 28px rgba(37,99,235,0.4);
}

.btn-danger {
    background:
        linear-gradient(
            135deg,
            #ef4444,
            #b91c1c
        );
}

.btn-success {
    background:
        linear-gradient(
            135deg,
            #10b981,
            #047857
        );
}

.btn-warning {
    background:
        linear-gradient(
            135deg,
            #f59e0b,
            #d97706
        );
}


/* ================= FORMS ================= */

label {
    color: #cbd5e1;
    font-size: 14px;
    font-weight: 600;
}

input,
select {

    width: 100%;

    padding: 13px 15px;

    margin: 8px 0 18px;

    border: 1px solid #334155;

    border-radius: 10px;

    background: #0f172a;

    color: #f8fafc;

    outline: none;

    font-size: 14px;

    transition: 0.2s;
}

input:focus,
select:focus {

    border-color: #60a5fa;

    box-shadow:
        0 0 0 3px rgba(96,165,250,0.12);
}

input::placeholder {
    color: #64748b;
}


/* ================= TABLE ================= */

table {

    width: 100%;

    border-collapse: separate;
    border-spacing: 0;

    background: rgba(15,23,42,0.9);

    margin-top: 20px;

    border-radius: 15px;

    overflow: hidden;

    border: 1px solid rgba(148,163,184,0.12);
}

th,
td {

    padding: 15px;

    border-bottom: 1px solid rgba(148,163,184,0.1);

    text-align: left;

    font-size: 14px;
}

th {

    background:
        linear-gradient(
            135deg,
            #1e3a8a,
            #4c1d95
        );

    color: white;

    font-weight: 700;
}

td {
    color: #cbd5e1;
}

tr:hover td {
    background: rgba(59,130,246,0.06);
}


/* ================= ALERT ================= */

.alert {

    padding: 14px 17px;

    background: rgba(127,29,29,0.35);

    color: #fecaca;

    border: 1px solid rgba(248,113,113,0.25);

    border-radius: 10px;

    margin-bottom: 15px;
}

.success {

    padding: 14px 17px;

    background: rgba(6,78,59,0.35);

    color: #a7f3d0;

    border: 1px solid rgba(52,211,153,0.2);

    border-radius: 10px;

    margin-bottom: 15px;
}


/* ================= LOGIN ================= */

.login-box {

    width: 410px;

    max-width: 92%;

    margin: 90px auto;

    background:
        linear-gradient(
            145deg,
            rgba(30,41,59,0.96),
            rgba(15,23,42,0.96)
        );

    padding: 38px;

    border-radius: 24px;

    border: 1px solid rgba(148,163,184,0.15);

    box-shadow:
        0 30px 80px rgba(0,0,0,0.45),
        0 0 40px rgba(59,130,246,0.08);
}

.login-box h2 {
    font-size: 28px;
    margin-bottom: 25px;
}

.login-box hr {
    border: none;
    border-top: 1px solid #334155;
    margin: 25px 0;
}

.login-box p {
    color: #94a3b8;
    font-size: 13px;
}


/* ================= CENTER ================= */

.center {
    text-align: center;
}


/* ================= HOME HERO ================= */

.hero {

    padding: 70px 30px;

    text-align: center;

    border-radius: 28px;

    background:
        radial-gradient(
            circle at top,
            rgba(59,130,246,0.2),
            transparent 55%
        ),
        linear-gradient(
            145deg,
            #0f172a,
            #111827
        );

    border: 1px solid rgba(96,165,250,0.15);

    box-shadow:
        0 30px 80px rgba(0,0,0,0.35);
}

.hero h1 {

    font-size: 42px;

    background:
        linear-gradient(
            90deg,
            #60a5fa,
            #a78bfa,
            #22d3ee
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {

    max-width: 700px;

    margin: 15px auto 30px;

    color: #94a3b8;

    font-size: 16px;

    line-height: 1.7;
}


/* ================= MOBILE ================= */

@media (max-width: 768px) {

    .navbar {
        padding: 15px;
        flex-direction: column;
        gap: 12px;
    }

    .navbar div {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
    }

    .navbar a {
        margin: 5px 8px;
    }

    .container {
        width: 94%;
    }

    h1 {
        font-size: 27px;
    }

    .hero h1 {
        font-size: 30px;
    }

    table {
        display: block;
        overflow-x: auto;
        white-space: nowrap;
    }

}

</style>
"""

# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template_string("""
    {{ style|safe }}

    <div class="navbar">
        <h2>🚌 College Bus Tracking System</h2>
        <a href="/login">Login</a>
    </div>

    <div class="container">

        <div class="container">

    <div class="hero">

        <div style="font-size:60px;">
            🚌
        </div>

        <h1>
            College Bus Tracking System
        </h1>

        <p>
            Smart transportation platform for
            real-time bus tracking, QR attendance,
            AI-powered ETA and instant parent notifications.
        </p>

        <a class="btn" href="/login">
            🚀 Enter System
        </a>

    </div>

</div>azccxxxC

            <h1>College Bus Tracking & Parent Notification System</h1>

            <p>
                Smart system for student attendance,
                bus tracking and parent notifications.
            </p>

            <a class="btn" href="/login">
                Login
            </a>

        </div>

    </div>

    """, style=STYLE)


# =========================================================
# LOGIN
# =========================================================
@app.route("/login", methods=["GET", "POST"])
def login():

    error = ""

    if request.method == "POST":

        role = request.form.get("role")
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # ================= ADMIN LOGIN =================
        if role == "admin":

            if username == "admin" and password == "admin123":

                session.clear()
                session["user_role"] = "admin"
                session["username"] = "Administrator"

                return redirect("/admin-dashboard")

            error = "Invalid Admin Username or Password!"

        # ================= STUDENT LOGIN =================
        elif role == "student":

            connection = get_connection()

            student = connection.execute("""
                SELECT *
                FROM students
                WHERE college_id = ?
            """, (username,)).fetchone()

            connection.close()

            if student:

                db_roll = str(student["roll_number"]).strip()

                if password == db_roll:

                    session.clear()

                    session["user_role"] = "student"
                    session["college_id"] = student["college_id"]
                    session["username"] = student["name"]

                    return redirect("/student-dashboard")

            error = "Invalid Student College ID or Roll Number!"

        # ================= PARENT LOGIN =================
        elif role == "parent":

            college_id = username
            phone = password

            connection = get_connection()

            student = connection.execute("""
                SELECT *
                FROM students
                WHERE college_id = ?
            """, (college_id,)).fetchone()

            connection.close()

            if student:

                db_phone = str(
                    student["parent_phone"] or ""
                ).strip()

                # Remove Excel .0
                if db_phone.endswith(".0"):
                    db_phone = db_phone[:-2]

                # Keep digits only
                db_phone_clean = "".join(
                    ch for ch in db_phone
                    if ch.isdigit()
                )

                entered_phone_clean = "".join(
                    ch for ch in phone
                    if ch.isdigit()
                )

                if entered_phone_clean == db_phone_clean:

                    session.clear()

                    session["user_role"] = "parent"
                    session["college_id"] = student["college_id"]
                    session["username"] = student["parent_name"]

                    return redirect("/parent-dashboard")

            error = "Invalid Parent College ID or Parent Phone!"

    return render_template_string("""
    
    {{ style|safe }}

    <div class="navbar">
        <h2>🚌 College Bus Tracking System</h2>
        <a href="/">Home</a>
    </div>

    <div class="login-box">

        <div class="center">

            <div style="font-size:50px;">🚌</div>

            <h2>Welcome Back</h2>

            <p style="color:#64748b;">
                Login to your bus tracking system
            </p>

        </div>

        {% if error %}
            <div class="alert">
                ❌ {{ error }}
            </div>
        {% endif %}

        <form method="POST">

            <label>Login As</label>

            <select name="role" required>
                <option value="admin">Admin</option>
                <option value="student">Student</option>
                <option value="parent">Parent</option>
            </select>

            <label>College ID / Username</label>

            <input
                type="text"
                name="username"
                placeholder="Enter College ID"
                required
            >

            <label>Password</label>

            <input
                type="password"
                name="password"
                placeholder="Enter password"
                required
            >

            <button
                type="submit"
                class="btn"
                style="width:100%; margin:10px 0 0 0;"
            >
                🔐 Login
            </button>

        </form>

    </div>

    """, style=STYLE)


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin-dashboard")
@login_required("admin")
def admin_dashboard():

    connection = get_connection()

    student_count = connection.execute(
        "SELECT COUNT(*) AS count FROM students"
    ).fetchone()["count"]

    bus_count = connection.execute(
        "SELECT COUNT(*) AS count FROM buses"
    ).fetchone()["count"]

    attendance_count = connection.execute(
        "SELECT COUNT(*) AS count FROM attendance"
    ).fetchone()["count"]

    notification_count = connection.execute(
        "SELECT COUNT(*) AS count FROM notifications"
    ).fetchone()["count"]

    connection.close()

    return render_template_string("""

    {{ style|safe }}

    <div class="navbar">

        <h2>🚌 Admin Dashboard</h2>

        <div>
            <a href="/admin-dashboard">Home</a>
            <a href="/students">Students</a>
            <a href="/buses">Buses</a>
            <a href="/attendance">Attendance</a>
            <a href="/scan">QR Scanner</a>
            <a href="/tracking">Tracking</a>
            <a href="/reports">Reports</a>
            <a href="/logout">Logout</a>
        </div>

    </div>


    <div class="container">

        <h1>Welcome Admin 👋</h1>

        <div class="card-container">

            <div class="card">
                <h3>👨‍🎓 Total Students</h3>
                <div class="stat">
                    {{ student_count }}
                </div>
            </div>

            <div class="card">
                <h3>🚌 Total Buses</h3>
                <div class="stat">
                    {{ bus_count }}
                </div>
            </div>

            <div class="card">
                <h3>📋 Attendance Records</h3>
                <div class="stat">
                    {{ attendance_count }}
                </div>
            </div>

            <div class="card">
                <h3>🔔 Notifications</h3>
                <div class="stat">
                    {{ notification_count }}
                </div>
            </div>

        </div>


        <br>

        <div class="card">

            <h2>Quick Actions</h2>

            <a class="btn" href="/students">
                👨‍🎓 Manage Students
            </a>

            <a class="btn" href="/buses">
                🚌 Manage Buses
            </a>

            <a class="btn" href="/scan">
                📷 Scan QR
            </a>

            <a class="btn" href="/attendance">
                📋 Attendance
            </a>

            <a class="btn" href="/tracking">
                📍 Bus Tracking
            </a>

            <a class="btn" href="/reports">
                📊 Reports
            </a>

        </div>

    </div>

    """,
    style=STYLE,
    student_count=student_count,
    bus_count=bus_count,
    attendance_count=attendance_count,
    notification_count=notification_count)


# =========================================================
# STUDENTS
# =========================================================

@app.route("/students")
@login_required("admin")
def students():

    connection = get_connection()

    students_list = connection.execute("""
        SELECT
            students.*,
            buses.bus_number
        FROM students
        LEFT JOIN buses
        ON students.bus_id = buses.bus_id
        ORDER BY students.college_id
    """).fetchall()

    connection.close()

    return render_template_string("""

    {{ style|safe }}

    <div class="navbar">

        <h2>👨‍🎓 Student Management</h2>

        <div>
            <a href="/admin-dashboard">Dashboard</a>
            <a href="/logout">Logout</a>
        </div>

    </div>


    <div class="container">

        <a class="btn btn-success" href="/add-student">
            + Add Student
        </a>

        <table>

            <tr>
                <th>College ID</th>
                <th>Name</th>
                <th>Roll Number</th>
                <th>Bus</th>
                <th>Parent</th>
                <th>Phone</th>
                <th>Action</th>
            </tr>

            {% for student in students_list %}

            <tr>

                <td>{{ student["college_id"] }}</td>

                <td>{{ student["name"] }}</td>

                <td>{{ student["roll_number"] }}</td>

                <td>
                    {{ student["bus_number"] or "Not Assigned" }}
                </td>

                <td>{{ student["parent_name"] }}</td>

                <td>{{ student["parent_phone"] }}</td>

                <td>

                    <a class="btn btn-warning"
                       href="/edit-student/{{ student['student_id'] }}">
                       Edit
                    </a>

                    <a class="btn btn-danger"
                       href="/delete-student/{{ student['student_id'] }}"
                       onclick="return confirm('Delete this student?')">
                       Delete
                    </a>

                </td>

            </tr>

            {% endfor %}

        </table>

    </div>

    """,
    style=STYLE,
    students_list=students_list)


# =========================================================
# ADD STUDENT
# =========================================================

@app.route("/add-student", methods=["GET", "POST"])
@login_required("admin")
def add_student():

    connection = get_connection()

    buses = connection.execute(
        "SELECT * FROM buses"
    ).fetchall()

    if request.method == "POST":

        college_id = request.form["college_id"]
        name = request.form["name"]
        roll_number = request.form["roll_number"]
        bus_id = request.form["bus_id"]
        parent_name = request.form["parent_name"]
        parent_phone = request.form["parent_phone"]

        try:

            connection.execute("""
                INSERT INTO students
                (
                    college_id,
                    name,
                    roll_number,
                    bus_id,
                    parent_name,
                    parent_phone
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                college_id,
                name,
                roll_number,
                bus_id,
                parent_name,
                parent_phone
            ))

            connection.commit()
            connection.close()

            return redirect("/students")

        except sqlite3.IntegrityError:

            connection.close()

            return "College ID or Roll Number already exists!"

    connection.close()

    return render_template_string("""

    {{ style|safe }}

    <div class="container">

        <div class="card">

            <h2>➕ Add Student</h2>

            <form method="POST">

                <label>College ID</label>
                <input type="number"
                       name="college_id"
                       required>

                <label>Name</label>
                <input type="text"
                       name="name"
                       required>

                <label>Roll Number</label>
                <input type="text"
                       name="roll_number"
                       required>

                <label>Bus</label>

                <select name="bus_id">

                    <option value="">
                        Select Bus
                    </option>

                    {% for bus in buses %}

                    <option value="{{ bus['bus_id'] }}">
                        {{ bus['bus_number'] }}
                    </option>

                    {% endfor %}

                </select>

                <label>Parent Name</label>
                <input type="text"
                       name="parent_name">

                <label>Parent Phone</label>
                <input type="text"
                       name="parent_phone">

                <button class="btn btn-success">
                    Save Student
                </button>

                <a class="btn"
                   href="/students">
                   Cancel
                </a>

            </form>

        </div>

    </div>

    """,
    style=STYLE,
    buses=buses)


# =========================================================
# EDIT STUDENT
# =========================================================

@app.route("/edit-student/<int:student_id>", methods=["GET", "POST"])
@login_required("admin")
def edit_student(student_id):

    connection = get_connection()

    student = connection.execute("""
        SELECT *
        FROM students
        WHERE student_id = ?
    """, (student_id,)).fetchone()

    buses = connection.execute(
        "SELECT * FROM buses"
    ).fetchall()

    if not student:

        connection.close()

        return "Student not found!"

    if request.method == "POST":

        connection.execute("""
            UPDATE students
            SET
                college_id = ?,
                name = ?,
                roll_number = ?,
                bus_id = ?,
                parent_name = ?,
                parent_phone = ?
            WHERE student_id = ?
        """, (
            request.form["college_id"],
            request.form["name"],
            request.form["roll_number"],
            request.form["bus_id"],
            request.form["parent_name"],
            request.form["parent_phone"],
            student_id
        ))

        connection.commit()
        connection.close()

        return redirect("/students")

    connection.close()

    return render_template_string("""

    {{ style|safe }}

    <div class="container">

        <div class="card">

            <h2>✏️ Edit Student</h2>

            <form method="POST">

                <label>College ID</label>

                <input type="number"
                       name="college_id"
                       value="{{ student['college_id'] }}"
                       required>


                <label>Name</label>

                <input type="text"
                       name="name"
                       value="{{ student['name'] }}"
                       required>


                <label>Roll Number</label>

                <input type="text"
                       name="roll_number"
                       value="{{ student['roll_number'] }}"
                       required>


                <label>Bus</label>

                <select name="bus_id">

                    {% for bus in buses %}

                    <option value="{{ bus['bus_id'] }}"
                    {% if bus['bus_id'] == student['bus_id'] %}
                    selected
                    {% endif %}>

                        {{ bus['bus_number'] }}

                    </option>

                    {% endfor %}

                </select>


                <label>Parent Name</label>

                <input type="text"
                       name="parent_name"
                       value="{{ student['parent_name'] }}">


                <label>Parent Phone</label>

                <input type="text"
                       name="parent_phone"
                       value="{{ student['parent_phone'] }}">


                <button class="btn btn-success">
                    Update Student
                </button>

            </form>

        </div>

    </div>

    """,
    style=STYLE,
    student=student,
    buses=buses)


# =========================================================
# DELETE STUDENT
# =========================================================

@app.route("/delete-student/<int:student_id>")
@login_required("admin")
def delete_student(student_id):

    connection = get_connection()

    connection.execute("""
        DELETE FROM students
        WHERE student_id = ?
    """, (student_id,))

    connection.commit()
    connection.close()

    return redirect("/students")


# =========================================================
# BUS LIST
# =========================================================

@app.route("/buses")
@login_required("admin")
def buses():

    connection = get_connection()

    buses_list = connection.execute("""
        SELECT *
        FROM buses
        ORDER BY bus_id
    """).fetchall()

    connection.close()

    return render_template_string("""

    {{ style|safe }}

    <div class="navbar">

        <h2>🚌 Bus Management</h2>

        <a href="/admin-dashboard">
            Dashboard
        </a>

    </div>

    <div class="container">

        <a class="btn btn-success"
           href="/add-bus">
           + Add Bus
        </a>

        <table>

            <tr>
                <th>ID</th>
                <th>Bus Number</th>
                <th>Driver</th>
                <th>Route</th>
                <th>Action</th>
            </tr>

            {% for bus in buses_list %}

            <tr>

                <td>{{ bus["bus_id"] }}</td>

                <td>{{ bus["bus_number"] }}</td>

                <td>{{ bus["driver_name"] }}</td>

                <td>{{ bus["route"] }}</td>

                <td>

                    <a class="btn btn-warning"
                       href="/edit-bus/{{ bus['bus_id'] }}">
                       Edit
                    </a>

                    <a class="btn btn-danger"
                       href="/delete-bus/{{ bus['bus_id'] }}"
                       onclick="return confirm('Delete this bus?')">
                       Delete
                    </a>

                </td>

            </tr>

            {% endfor %}

        </table>

    </div>

    """,
    style=STYLE,
    buses_list=buses_list)


# =========================================================
# ADD BUS
# =========================================================

@app.route("/add-bus", methods=["GET", "POST"])
@login_required("admin")
def add_bus():

    if request.method == "POST":

        bus_number = request.form["bus_number"]
        driver_name = request.form["driver_name"]
        route = request.form["route"]

        connection = get_connection()

        connection.execute("""
            INSERT INTO buses
            (
                bus_number,
                driver_name,
                route
            )
            VALUES (?, ?, ?)
        """, (
            bus_number,
            driver_name,
            route
        ))

        connection.commit()
        connection.close()

        return redirect("/buses")

    return render_template_string("""

    {{ style|safe }}

    <div class="container">

        <div class="card">

            <h2>➕ Add Bus</h2>

            <form method="POST">

                <label>Bus Number</label>
                <input type="text"
                       name="bus_number"
                       required>

                <label>Driver Name</label>
                <input type="text"
                       name="driver_name"
                       required>

                <label>Route</label>
                <input type="text"
                       name="route"
                       required>

                <button class="btn btn-success">
                    Save Bus
                </button>

            </form>

        </div>

    </div>

    """, style=STYLE)


# =========================================================
# EDIT BUS
# =========================================================

@app.route("/edit-bus/<int:bus_id>", methods=["GET", "POST"])
@login_required("admin")
def edit_bus(bus_id):

    connection = get_connection()

    bus = connection.execute("""
        SELECT *
        FROM buses
        WHERE bus_id = ?
    """, (bus_id,)).fetchone()

    if not bus:

        connection.close()

        return "Bus not found!"

    if request.method == "POST":

        connection.execute("""
            UPDATE buses
            SET
                bus_number = ?,
                driver_name = ?,
                route = ?
            WHERE bus_id = ?
        """, (
            request.form["bus_number"],
            request.form["driver_name"],
            request.form["route"],
            bus_id
        ))

        connection.commit()
        connection.close()

        return redirect("/buses")

    connection.close()

    return render_template_string("""

    {{ style|safe }}

    <div class="container">

        <div class="card">

            <h2>✏️ Edit Bus</h2>

            <form method="POST">

                <label>Bus Number</label>

                <input type="text"
                       name="bus_number"
                       value="{{ bus['bus_number'] }}"
                       required>


                <label>Driver Name</label>

                <input type="text"
                       name="driver_name"
                       value="{{ bus['driver_name'] }}"
                       required>


                <label>Route</label>

                <input type="text"
                       name="route"
                       value="{{ bus['route'] }}"
                       required>


                <button class="btn btn-success">
                    Update Bus
                </button>

            </form>

        </div>

    </div>

    """,
    style=STYLE,
    bus=bus)


# =========================================================
# DELETE BUS
# =========================================================

@app.route("/delete-bus/<int:bus_id>")
@login_required("admin")
def delete_bus(bus_id):

    connection = get_connection()

    connection.execute("""
        DELETE FROM buses
        WHERE bus_id = ?
    """, (bus_id,))

    connection.commit()
    connection.close()

    return redirect("/buses")


# =========================================================
# ATTENDANCE
# =========================================================

@app.route("/attendance")
@login_required("admin")
def attendance():

    connection = get_connection()

    records = connection.execute("""
        SELECT
            attendance.attendance_id,
            students.college_id,
            students.name,
            students.roll_number,
            attendance.date,
            attendance.status
        FROM attendance
        JOIN students
        ON attendance.student_id = students.student_id
        ORDER BY attendance.attendance_id DESC
    """).fetchall()

    connection.close()

    return render_template_string("""

    {{ style|safe }}

    <div class="navbar">

        <h2>📋 Attendance</h2>

        <a href="/admin-dashboard">
            Dashboard
        </a>

    </div>

    <div class="container">

        <table>

            <tr>
                <th>ID</th>
                <th>College ID</th>
                <th>Name</th>
                <th>Roll Number</th>
                <th>Date</th>
                <th>Status</th>
            </tr>

            {% for record in records %}

            <tr>

                <td>{{ record["attendance_id"] }}</td>

                <td>{{ record["college_id"] }}</td>

                <td>{{ record["name"] }}</td>

                <td>{{ record["roll_number"] }}</td>

                <td>{{ record["date"] }}</td>

                <td>{{ record["status"] }}</td>

            </tr>

            {% endfor %}

        </table>

    </div>

    """,
    style=STYLE,
    records=records)


# =========================================================
# QR SCANNER
# =========================================================
@app.route("/scan")
@login_required("admin")
def scan():

    return render_template_string("""

    {{ style|safe }}

    <div class="navbar">

        <h2>📷 Student QR Scanner</h2>

        <a href="/admin-dashboard">
            Dashboard
        </a>

    </div>

    <div class="container">

        <div class="card center">

            <h2>Scan Student QR</h2>

            <div id="reader"
                 style="width:100%; max-width:500px; margin:auto;">
            </div>

            <br>

            <h3>Or enter College ID manually</h3>

            <input
                id="college_id"
                type="text"
                placeholder="Enter College ID"
            >

            <button
                class="btn"
                type="button"
                onclick="manualSearch()"
            >
                🔍 Search
            </button>

        </div>

        <div id="result"></div>

    </div>

    <script
        src="https://unpkg.com/html5-qrcode"
        type="text/javascript">
    </script>

    <script>

    function processCollegeID(collegeID) {

        collegeID = collegeID.trim();

        if (!collegeID) {
            return;
        }

        fetch("/api/student/" + encodeURIComponent(collegeID))

        .then(response => response.json())

        .then(data => {

            let result =
                document.getElementById("result");

            if (data.success) {

                result.innerHTML = `

                    <div class="card">

                        <h2>✅ Student Found</h2>

                        <p>
                            <b>College ID:</b>
                            ${data.student.college_id}
                        </p>

                        <p>
                            <b>Name:</b>
                            ${data.student.name}
                        </p>

                        <p>
                            <b>Roll Number:</b>
                            ${data.student.roll_number}
                        </p>

                        <p>
                            <b>Bus:</b>
                            ${data.student.bus_number}
                        </p>

                        <p>
                            <b>Parent:</b>
                            ${data.student.parent_name}
                        </p>

                        <p>
                            <b>Phone:</b>
                            ${data.student.parent_phone}
                        </p>

                        <div class="success">
                            ${data.notification}
                        </div>

                    </div>
                `;

            } else {

                result.innerHTML = `

                    <div class="alert">
                        ❌ ${data.message}
                    </div>

                `;
            }

        })

        .catch(error => {

            document.getElementById("result").innerHTML = `

                <div class="alert">
                    ❌ Unable to connect to server.
                </div>

            `;

            console.error(error);

        });

    }


    function manualSearch() {

        const collegeID =
            document.getElementById("college_id").value;

        processCollegeID(collegeID);

    }


    function onScanSuccess(decodedText) {

        processCollegeID(decodedText);

    }


    function onScanFailure(error) {

        // Scanner continues searching

    }


    const scanner =
        new Html5QrcodeScanner(
            "reader",
            {
                fps: 10,
                qrbox: 250
            }
        );


    scanner.render(
        onScanSuccess,
        onScanFailure
    );

    </script>

    """, style=STYLE)



# =========================================================
# QR API
# =========================================================


@app.route("/api/student/<int:college_id>")
@login_required("admin")
def get_student(college_id):

    connection = get_connection()

    student = connection.execute("""
        SELECT
            s.student_id,
            s.college_id,
            s.name,
            s.roll_number,
            s.parent_name,
            s.parent_phone,
            b.bus_number,
            b.route
        FROM students s
        LEFT JOIN buses bs
        ON s.bus_id = b.bus_id
        WHERE s.college_id = ?
    """, (college_id,)).fetchone()

    if not student:
        connection.close()

        return jsonify({
            "success": False,
            "message": "Student not found!"
        })

    student_id = student["student_id"]

    today = datetime.now().strftime("%Y-%m-%d")

    existing = connection.execute("""
        SELECT attendance_id
        FROM attendance
        WHERE student_id = ?
        AND date = ?
    """, (student_id, today)).fetchone()

    if not existing:

        connection.execute("""
            INSERT INTO attendance
            (student_id, date, status)
            VALUES (?, ?, ?)
        """, (
            student_id,
            today,
            "Present"
        ))

        message = (
            f"Student {student['name']} "
            f"has boarded the bus today."
        )

        connection.executse("""
            INSERT INTO notifications
            (student_id, message, notification_type, created_at, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            student_id,
            message,
            "Parent",
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Queued"
        ))

        notification = "Parent notification queued successfully."

    else:

        notification = "Attendance already marked today."

    connection.commit()
    connection.close()

    return jsonify({
        "success": True,

        "student": {
            "college_id": student["college_id"],
            "name": student["name"],
            "roll_number": student["roll_number"],
            "bus_number": student["bus_number"] or "Not Assigned",
            "route": student["route"] or "Not Assigned",
            "parent_name": student["parent_name"] or "Not Available",
            "parent_phone": student["parent_phone"] or "Not Available"
        },

        "notification": notification
    })
# =========================================================
# PARENT DASHBOARD
# =========================================================

@app.route("/parent-dashboard")
@login_required("parent")
def parent_dashboard():

    college_id = session["college_id"]

    connection = get_connection()

    student = connection.execute("""
        SELECT
            students.*,
            buses.bus_number,
            buses.route
        FROM students
        LEFT JOIN buses
        ON students.bus_id = buses.bus_id
        WHERE students.college_id = ?
    """, (college_id,)).fetchone()


    attendance_records = connection.execute("""
        SELECT *
        FROM attendance
        WHERE student_id = ?
        ORDER BY attendance_id DESC
        LIMIT 10
    """, (student["student_id"],)).fetchall()


    notifications = connection.execute("""
        SELECT *
        FROM notifications
        WHERE student_id = ?
        ORDER BY notification_id DESC
        LIMIT 10
    """, (student["student_id"],)).fetchall()


    connection.close()


    return render_template_string("""

    {{ style|safe }}

    <div class="navbar">

        <h2>👨‍👩‍👧 Parent Dashboard</h2>

        <a href="/logout">
            Logout
        </a>

    </div>


    <div class="container">

        <h1>
            Welcome {{ student["parent_name"] }} 👋
        </h1>


        <div class="card-container">

            <div class="card">

                <h3>Student</h3>

                <p>
                {{ student["name"] }}
                </p>

            </div>


            <div class="card">

                <h3>College ID</h3>

                <p>
                {{ student["college_id"] }}
                </p>

            </div>


            <div class="card">

                <h3>Bus</h3>

                <p>
                {{ student["bus_number"] or "Not Assigned" }}
                </p>

            </div>


            <div class="card">

                <h3>Route</h3>

                <p>
                {{ student["route"] or "Not Available" }}
                </p>

            </div>

        </div>


        <br>


        <div class="card">

            <h2>📋 Recent Attendance</h2>

            <table>

                <tr>
                    <th>Date</th>
                    <th>Status</th>
                </tr>

                {% for record in attendance_records %}

                <tr>

                    <td>
                        {{ record["date"] }}
                    </td>

                    <td>
                        {{ record["status"] }}
                    </td>

                </tr>

                {% endfor %}

            </table>

        </div>


        <br>


        <div class="card">

            <h2>🔔 Notifications</h2>

            {% for notification in notifications %}

                <div class="success">

                    <b>
                    {{ notification["created_at"] }}
                    </b>

                    <br>

                    {{ notification["message"] }}

                </div>

            {% endfor %}

        </div>

    </div>

    """,
    style=STYLE,
    student=student,
    attendance_records=attendance_records,
    notifications=notifications)


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@app.route("/student-dashboard")
@login_required("student")
def student_dashboard():

    college_id = session["college_id"]

    connection = get_connection()

    student = connection.execute("""
        SELECT
            students.*,
            buses.bus_number,
            buses.route
        FROM students
        LEFT JOIN buses
        ON students.bus_id = buses.bus_id
        WHERE students.college_id = ?
    """, (college_id,)).fetchone()


    attendance_records = connection.execute("""
        SELECT *
        FROM attendance
        WHERE student_id = ?
        ORDER BY attendance_id DESC
    """, (student["student_id"],)).fetchall()


    connection.close()


    return render_template_string("""

    {{ style|safe }}

    <div class="navbar">

        <h2>🎓 Student Dashboard</h2>

        <a href="/logout">
            Logout
        </a>

    </div>


    <div class="container">

        <div class="card">

            <h2>
                Welcome {{ student["name"] }} 👋
            </h2>

            <p>
                <b>College ID:</b>
                {{ student["college_id"] }}
            </p>

            <p>
                <b>Roll Number:</b>
                {{ student["roll_number"] }}
            </p>

            <p>
                <b>Bus:</b>
                {{ student["bus_number"] or "Not Assigned" }}
            </p>

            <p>
                <b>Route:</b>
                {{ student["route"] or "Not Available" }}
            </p>

        </div>


        <br>


        <div class="card">

            <h2>📋 Attendance</h2>

            <table>

                <tr>
                    <th>Date</th>
                    <th>Status</th>
                </tr>

                {% for record in attendance_records %}

                <tr>

                    <td>
                        {{ record["date"] }}
                    </td>

                    <td>
                        {{ record["status"] }}
                    </td>

                </tr>

                {% endfor %}

            </table>

        </div>

    </div>

    """,
    style=STYLE,
    student=student,
    attendance_records=attendance_records)


# =========================================================
# BUS TRACKING
# =========================================================

@app.route("/tracking")
@login_required("admin")
def tracking():

    connection = get_connection()

    buses_list = connection.execute("""
        SELECT
            b.bus_id,
            b.bus_number,
            b.driver_name,
            b.route,
            bl.latitude,
            bl.longitude,
            bl.status,
            bl.updated_at
        FROM buses b
        LEFT JOIN bus_locations bl
        ON b.bus_id = bl.bus_id
        AND bl.updated_at = (
            SELECT MAX(updated_at)
            FROM bus_locations
            WHERE bus_id = b.bus_id
        )
        ORDER BY b.bus_id
    """).fetchall()

    connection.close()

    destination_latitude = 10.8050
    destination_longitude = 78.7200

    updated_buses = []

    from math import radians, sin, cos, sqrt, atan2

    for bus in buses_list:

        bus_data = dict(bus)

        # Default values
        bus_data["distance"] = None
        bus_data["speed"] = None
        bus_data["eta"] = None

        if bus["latitude"] is not None and bus["longitude"] is not None:

            lat1 = radians(float(bus["latitude"]))
            lat2 = radians(destination_latitude)

            delta_lat = radians(
                destination_latitude - float(bus["latitude"])
            )

            delta_lon = radians(
                destination_longitude - float(bus["longitude"])
            )

            a = (
                sin(delta_lat / 2) ** 2
                + cos(lat1)
                * cos(lat2)
                * sin(delta_lon / 2) ** 2
            )

            c = 2 * atan2(
                sqrt(a),
                sqrt(1 - a)
            )

            distance = 6371 * c

            # Current demo speed
            speed = 30

            prediction = model.predict(
                [[distance, speed]]
            )

            bus_data["distance"] = round(distance, 2)
            bus_data["speed"] = speed
            bus_data["eta"] = round(
                float(prediction[0]), 2
            )

        updated_buses.append(bus_data)

    return render_template_string("""

    {{ style|safe }}

    <div class="navbar">

        <h2>📍 Real-Time Bus Tracking</h2>

        <a href="/admin-dashboard">
            Dashboard
        </a>

    </div>

    <div class="container">

        <div class="card">

            <h2>🚌 Live Bus Locations + AI ETA</h2>

            <table>

                <tr>
                    <th>Bus ID</th>
                    <th>Bus Number</th>
                    <th>Driver</th>
                    <th>Route</th>
                    <th>Latitude</th>
                    <th>Longitude</th>
                    <th>GPS Status</th>
                    <th>Distance</th>
                    <th>Speed</th>
                    <th>AI ETA</th>
                    <th>Last Updated</th>
                </tr>

s                {% for bus in buses_list %}

                <tr>

                    <td>{{ bus["bus_id"] }}</td>
                    <td>{{ bus["bus_number"] }}</td>
                    <td>{{ bus["driver_name"] }}</td>
                    <td>{{ bus["route"] }}</td>

                    <td>
 s                       {% if bus["latitude"] is not none %}
                            {{ bus["latitude"] }}
                        {% else %}
                            -
                        {% endif %}
                    </td>

                    <td>
                        {% if bus["longitude"] is not none %}
                            {{ bus["longitude"] }}
                        {% else %}
                            -
                        {% endif %}
                    </td>

                    <td>
                        {% if bus["status"] %}
                            🟢 {{ bus["status"] }}
                        {% else %}
                            🟡 Waiting
                        {% endif %}
                    </td>

                    <td>
                        {% if bus["distance"] is not none %}
                            {{ bus["distance"] }} km
                        {% else %}
                            -
                        {% endif %}
                    </td>

                    <td>
                        {% if bus["speed"] is not none %}
                            {{ bus["speed"] }} km/h
                        {% else %}
                            -
                        {% endif %}
                    </td>

                    <td>
                        {% if bus["eta"] is not none %}
                            🤖 {{ bus["eta"] }} min
                        {% else %}
                            -
                        {% endif %}
                    </td>

                    <td>
                        {% if bus["updated_at"] %}
                            {{ bus["updated_at"] }}
                        {% else %}
                            -
                        {% endif %}
                    </td>

                </tr>

                {% endfor %}

            </table>

        </div>

    </div>

    """,
    style=STYLE,
    buses_list=updated_buses)

# =========================================================
# REPORTS
# =========================================================

@app.route("/reports")
@login_required("admin")
def reports():

    today = datetime.now().strftime("%Y-%m-%d")

    connection = get_connection()

    total_students = connection.execute(
        "SELECT COUNT(*) AS count FROM students"
    ).fetchone()["count"]

    total_buses = connection.execute(
        "SELECT COUNT(*) AS count FROM buses"
    ).fetchone()["count"]

    present = connection.execute("""
        SELECT COUNT(*) AS count
        FROM attendance
        WHERE date = ?
        AND status = 'Present'
    """, (today,)).fetchone()["count"]

    absent = connection.execute("""
        SELECT COUNT(*) AS count
        FROM attendance
        WHERE date = ?
        AND status = 'Absent'
    """, (today,)).fetchone()["count"]

    connection.close()

    return render_template_string("""

    {{ style|safe }}

    <div class="navbar">

        <h2>📊 Reports</h2>

        <a href="/admin-dashboard">
            Dashboard
        </a>

    </div>


    <div class="container">

        <div class="card-container">

            <div class="card">

                <h3>Total Students</h3>

                <div class="stat">
                    {{ total_students }}
                </div>

            </div>


            <div class="card">

                <h3>Total Buses</h3>

                <div class="stat">
                    {{ total_buses }}
                </div>

            </div>


            <div class="card">

                <h3>Present Today</h3>

                <div class="stat">
                    {{ present }}
                </div>

            </div>


            <div class="card">

                <h3>Absent Today</h3>

                <div class="stat">
                    {{ absent }}
                </div>

            </div>

        </div>

    </div>

    """,
    style=STYLE,
    total_students=total_students,
    total_buses=total_buses,
    present=present,
    absent=absent)


# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    init_database()

    print("")
    print("==========================================")
    print("  COLLEGE BUS TRACKING SYSTEM")
    print("==========================================")
    print("")
    print("Admin Login")
    print("Username : admin")
    print("Password : admin123")
    print("")
    print("Server running...")
    print("http://127.0.0.1:5000")
    print("==========================================")

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )