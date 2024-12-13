# Project Title
Student Exam System

## Description
A comprehensive system to manage students, semesters, exams, and result categories for a university or academic institution.

## Installation
```cmd
pip install -r requirements.txt
```

## Configuration
Set the following environment variables for the application:
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Secret key for JWT authentication

## API Endpoints
| Endpoint                     | Method | Description                                   |
|------------------------------|--------|-----------------------------------------------|
| `/register`                  | POST   | Register a new user                          |
| `/login`                     | POST   | Authenticate user and retrieve JWT token     |
| `/add_student`               | POST   | Add a new student (Administrator only)       |
| `/add_semester`              | POST   | Add a new semester (Administrator only)      |
| `/add_exam`                  | POST   | Add a new exam (Teacher/Administrator only)  |
| `/add_result_category`       | POST   | Add a new result category (Administrator only)|
| `/view_all_students`         | GET    | View all students (Teacher/Admin only)       |
| `/view_student/<student_id>` | GET    | View a specific student                      |
| `/view_semesters`            | GET    | View all semesters                           |
| `/view_exams`                | GET    | View all exams                               |
| `/view_result_categories`    | GET    | View all result categories                   |
| `/update_student/<id>`       | PUT    | Update a student (Administrator only)        |
| `/update_semester/<id>`      | PUT    | Update a semester (Administrator only)       |
| `/update_exam/<id>`          | PUT    | Update an exam                               |
| `/update_result_category/<code>` | PUT | Update a result category (Administrator only)|
| `/delete_student/<id>`       | DELETE | Delete a student (Administrator only)        |

## Testing
Run tests using the following command:
```cmd
pytest
```

## Git Commit Guidelines
Adhere to conventional commit messages for clarity and consistency:

- **feat**: New features (e.g., `feat: add user authentication`)
- **fix**: Bug fixes (e.g., `fix: resolve database connection issue`)
- **docs**: Documentation updates (e.g., `docs: update API documentation`)
- **test**: Adding or updating tests (e.g., `test: add user registration tests`)

## Code Overview

### Dependencies
- `Flask`: For creating APIs
- `mysql.connector`: For database connectivity
- `bcrypt`: For password hashing
- `jwt`: For user authentication

### Key Features

#### User Registration and Login
- Secure password hashing with bcrypt
- JWT token generation and validation

#### Role-Based Access Control
- Roles: `administrator`, `teacher`, and `student`
- Role checks with decorators (`@role_required`)

#### CRUD Operations
- **Students**: Add, view, update, and delete students
- **Semesters**: Add, view, and update semesters
- **Exams**: Add, view, and update exams
- **Result Categories**: Add, view, and update result categories

#### Error Handling
- Consistent error messages using `handle_error` function

#### Database Management
- MySQL for storing application data
- JSON file for initial user authentication setup

### Example Snippets
#### Token Validation Middleware
```python
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Token is missing or malformed!"}), 401

        try:
            token = token.split()[1]
            decoded = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            request.user = decoded
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired!"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token!"}), 401

        return f(*args, **kwargs)
    return decorated
```

#### Add Student Endpoint
```python
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
