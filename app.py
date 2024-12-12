from flask import Flask, request, jsonify
import jwt
import datetime
import mysql.connector
import json
from flask_bcrypt import Bcrypt
from functools import wraps

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config["DB_HOST"] = "localhost"
app.config["DB_USER"] = "root"
app.config["DB_PASSWORD"] = "root"
app.config["DB_NAME"] = "student_exam_system"
app.config["SECRET_KEY"] = "tian427618359"
app.config["USERS_FILE"] = "users.json"

def get_db_connection():
    conn = mysql.connector.connect(
        host=app.config["DB_HOST"],
        user=app.config["DB_USER"],
        password=app.config["DB_PASSWORD"],
        database=app.config["DB_NAME"]
    )
    return conn

# error handler
def handle_error(error_msg, status_code):
    return jsonify({"error": error_msg}), status_code

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Token is missing or malformed!"}), 401

        try:
            # Remove 'Bearer ' prefix
            token = token.split()[1]
            decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401

        return f(*args, **kwargs)
    return decorated


def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user_role = request.user.get("role", None)
            if user_role not in allowed_roles:
                return jsonify({"error": "Access forbidden: insufficient role"}), 403
            return f(*args, **kwargs)
        return wrapped
    return decorator

# users.json
users_data = {
    "users": []
}

def save_to_json():
    with open("users.json", "w") as f:
        json.dump(users_data, f)

def load_from_json():
    global users_data
    try:
        with open("users.json", "r") as f:
            users_data = json.load(f)
    except FileNotFoundError:
        save_to_json() 

# user registration
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password") or not data.get("role"):
        return handle_error("Missing required fields: username, password, and role are mandatory", 400)

    username = data["username"]
    password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
    role = data["role"]

    load_from_json()

    for user in users_data["users"]:
        if user["username"] == username:
            return handle_error("Username already exists", 400)

    new_user = {"username": username, "password": password, "role": role}
    users_data["users"].append(new_user)
    save_to_json()

    return jsonify({"message": "User registered successfully"}), 201

# user login
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not data.get("username") or not data.get("password"):
        return handle_error("Missing required fields: username and password are mandatory", 400)

    username = data["username"]
    password = data["password"]

    load_from_json()

    for user in users_data["users"]:
        if user["username"] == username and bcrypt.check_password_hash(user["password"], password):
            token = jwt.encode(
                {
                    "user_id": username,
                    "role": user["role"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                },
                app.config["SECRET_KEY"],
                algorithm="HS256",
            )
            return jsonify({"token": token}), 200

    return handle_error("Invalid credentials", 401)

# ADDD ---------------------------------------------------------

@app.route("/add_student", methods=["POST"])
@token_required
@role_required(["administrator"])
def add_student():
    data = request.get_json()
    required_fields = ["first_name", "last_name", "sex", "email"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Student (first_name, last_name, sex, email) VALUES (%s, %s, %s, %s)",
            (data["first_name"], data["last_name"], data["sex"], data["email"])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Student added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/add_semester", methods=["POST"])
@token_required
@role_required(["administrator"])
def add_semester():
    data = request.get_json()
    if not all(data.get(field) for field in ["semester_name", "start_date", "end_date"]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Semester (semester_name, start_date, end_date) VALUES (%s, %s, %s)",
            (data["semester_name"], data["start_date"], data["end_date"])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Semester added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/add_exam", methods=["POST"])
@token_required
@role_required(["teacher", "administrator"])
def add_exam():
    data = request.get_json()
    if not all(data.get(field) for field in ["exam_date", "semester_id"]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Exam (exam_date, semester_id) VALUES (%s, %s)",
            (data["exam_date"], data["semester_id"])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Exam added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/add_result_category", methods=["POST"])
@token_required
@role_required(["administrator"])
def add_result_category():
    data = request.get_json()
    required_fields = ["category_code", "mark_low", "mark_high", "description"]

    if not all(data.get(field) for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO result_category (category_code, mark_low, mark_high, description) VALUES (%s, %s, %s, %s)",
            (data["category_code"], data["mark_low"], data["mark_high"], data["description"])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Result category added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# READ -----------------------------------------------------------

@app.route("/view_all_students", methods=["GET"])
@token_required
@role_required(["teacher", "administrator"])
def view_all_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Student")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    if not students:
        return jsonify({"error": "No students found"}), 404
    return jsonify(students)


@app.route("/view_student/<int:student_id>", methods=["GET"])
@token_required
@role_required(["teacher", "administrator", "student"])
def view_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Student WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    if student is None:
        return jsonify({"error": "Student not found"}), 404
    return jsonify(student)

@app.route("/view_semesters", methods=["GET"])
@token_required
@role_required(["teacher", "administrator", "student"])
def view_semester():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Semester")
        semesters = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({"semesters": semesters}), 200
    except:
        return jsonify({"error": "Failed to retrieve semesters"}), 500

@app.route("/view_exams", methods=["GET"])
@token_required
@role_required(["teacher", "administrator", "student"])
def view_exam():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Exam")
        exams = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({"exams": exams}), 200
    except:
        return jsonify({"error": "Failed to retrieve exams"}), 500

@app.route("/view_result_categories", methods=["GET"])
@token_required
@role_required(["teacher", "administrator", "student"])
def view_result_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM result_category")
        categories = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({"result_categories": categories}), 200
    except:
        return jsonify({"error": "Failed to retrieve result categories"}), 500


# UPDATE ------------------------------------------------------- 
@app.route("/update_student/<int:student_id>", methods=["PUT"])
@token_required
@role_required(["administrator"])
def update_student(student_id):
    data = request.get_json()

    if not all(data.get(field) for field in ["first_name", "last_name", "sex", "email"]):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Student
        SET first_name = %s, last_name = %s, sex = %s, email = %s
        WHERE student_id = %s
        """,
        (data["first_name"], data["last_name"], data["sex"], data["email"], student_id)
    )
    conn.commit()
    row_count = cursor.rowcount
    cursor.close()
    conn.close()

    return (jsonify({"message": "Student updated successfully"}), 200) if row_count else (jsonify({"error": "Student not found"}), 404)


@app.route("/update_semester/<int:semester_id>", methods=["PUT"])
@token_required
@role_required(["administrator"])
def update_semester(semester_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE Semester SET semester_name = %s, start_date = %s, end_date = %s WHERE semester_id = %s",
        (data.get("semester_name"), data.get("start_date"), data.get("end_date"), semester_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Semester not found or no changes made"}), 404
    return jsonify({"message": "Semester updated successfully"}), 200


@app.route("/update_exam/<int:exam_id>", methods=["PUT"])
@token_required
@role_required(["teacher", "administrator"])
def update_exam(exam_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE Exam SET exam_date = %s, semester_id = %s WHERE exam_id = %s",
        (data.get("exam_date"), data.get("semester_id"), exam_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Exam not found or no changes made"}), 404
    return jsonify({"message": "Exam updated successfully"}), 200


@app.route("/update_result_category/<string:category_code>", methods=["PUT"])
@token_required
@role_required(["administrator"])

def update_result_category(category_code):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE result_category SET mark_low = %s, mark_high = %s, description = %s WHERE category_code = %s",
        (data.get("mark_low"), data.get("mark_high"), data.get("description"), category_code)
    )

    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Result category not found or no changes made"}), 404
    return jsonify({"message": "Result category updated successfully"}), 200

# DELETE -----------------------------------------------------------

@app.route("/delete_student/<int:student_id>", methods=["DELETE"])
@token_required
@role_required(["administrator"])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Student WHERE student_id = %s", (student_id,))
    conn.commit()

    row_count = cursor.rowcount 
    cursor.close()
    conn.close()

    if row_count == 0:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"message": "Student deleted successfully"}), 200



@app.route("/delete_semester/<int:semester_id>", methods=["DELETE"])
@token_required
@role_required(["administrator"])
def delete_semester(semester_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Semester WHERE semester_id = %s", (semester_id,))
    
    conn.commit()
    row_count = cursor.rowcount
    cursor.close()
    conn.close()

    if row_count == 0:
        return jsonify({"error": "Semester not found"}), 404
    return jsonify({"message": "Semester deleted successfully"}), 200



@app.route("/delete_exam/<int:exam_id>", methods=["DELETE"])
@token_required
@role_required(["teacher", "administrator"])
def delete_exam(exam_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Exam WHERE exam_id = %s", (exam_id,))
    
    conn.commit()
    row_count = cursor.rowcount
    cursor.close()
    conn.close()

    if row_count == 0:
        return jsonify({"error": "Exam not found"}), 404
    return jsonify({"message": "Exam deleted successfully"}), 200


@app.route("/delete_result_category/<string:category_code>", methods=["DELETE"])
@token_required
@role_required(["administrator"])
def delete_result_category(category_code):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM result_category WHERE category_code = %s", (category_code,))
    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({"error": "Result category not found"}), 404
    return jsonify({"message": "Result category deleted successfully"}), 200

# ADDITIONAL READ JOINS ------------------------------------------------------

@app.route("/performance_summary/<int:student_id>", methods=["GET"])
@token_required
@role_required(["teacher", "administrator"])
def performance_summary(student_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.exam_id, e.exam_date, er.grade, rc.description 
            FROM Exam_Result er
            JOIN Exam e ON er.exam_id = e.exam_id
            JOIN Result_Category rc ON er.category_code = rc.category_code
            WHERE er.student_id = %s
        """, (student_id,))
        results = cursor.fetchall()
        conn.close()

        if not results:
            return jsonify({"error": "No data found"}), 404

        grades = [float(r["grade"]) for r in results]
        return jsonify({
            "exams": len(results),
            "average": sum(grades) / len(grades),
            "details": results
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/exam_results/<int:student_id>", methods=["GET"])
@token_required
@role_required(["teacher", "administrator"])
def view_exam_results(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
    SELECT 
    s.student_id, s.first_name, s.last_name, s.sex, s.email, e.exam_id, e.exam_date, e.semester_id, r.result_id,r.grade, rc.description AS result_category
    FROM Student s
    JOIN Exam_Result r ON s.student_id = r.student_id
    JOIN Exam e ON r.exam_id = e.exam_id
    JOIN Result_Category rc ON r.category_code = rc.category_code
    WHERE s.student_id = %s
    """, (student_id,))
    exam_results = cursor.fetchall()
    cursor.close()
    conn.close()
    if not exam_results:
        return jsonify({"error": "No exam results found for this student"}), 404
    return jsonify(exam_results)


if __name__ == "__main__":
    app.run(debug=True)

