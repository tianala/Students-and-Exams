from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

app.config['DB_HOST'] = 'localhost'
app.config['DB_USER'] = 'root'    
app.config['DB_PASSWORD'] = 'root'
app.config['DB_NAME'] = 'student_exam_system'

def get_db_connection():
    conn = mysql.connector.connect(
        host=app.config['DB_HOST'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'],
        database=app.config['DB_NAME']
    )
    return conn

@app.route('/student_exam_system/add_student', methods=['POST'])
def add_student():
    data = request.get_json()
    if not all(data.get(field) for field in ['first_name', 'last_name', 'sex', 'email']):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        conn.cursor().execute(
            "INSERT INTO Student (first_name, last_name, sex, email) VALUES (%s, %s, %s, %s)",
            (data['first_name'], data['last_name'], data['sex'], data['email'])
        )
        conn.commit()
        conn.close()
        return jsonify({'message': 'Student added'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/student_exam_system/all_students', methods=['GET'])
def view_all_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Student")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    if not students:
        return jsonify({'error': 'No students found'}), 404
    return jsonify(students)


@app.route('/student_exam_system/student/<int:student_id>', methods=['GET'])
def view_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Student WHERE student_id = %s", (student_id,))
    student = cursor.fetchone()
    cursor.close()
    conn.close()
    if student is None:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify(student)

@app.route('/student_exam_system/update_student/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()

    if not all(data.get(field) for field in ['first_name', 'last_name', 'sex', 'email']):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Student
        SET first_name = %s, last_name = %s, sex = %s, email = %s
        WHERE student_id = %s
        """,
        (data['first_name'], data['last_name'], data['sex'], data['email'], student_id)
    )
    conn.commit()
    row_count = cursor.rowcount
    cursor.close()
    conn.close()

    return (jsonify({'message': 'Student updated successfully'}), 200) if row_count else (jsonify({'error': 'Student not found'}), 404)


@app.route('/student_exam_system/delete_student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Student WHERE student_id = %s", (student_id,))
    conn.commit()

    row_count = cursor.rowcount 
    cursor.close()
    conn.close()

    if row_count == 0:
        return jsonify({'error': 'Student not found'}), 404
    return jsonify({'message': 'Student deleted successfully'}), 200

@app.route('/student_exam_system/add_semester', methods=['POST'])
def add_semester():
    try:
        data = request.get_json()
        if not all(data.get(field) for field in ['semester_name', 'start_date', 'end_date']):
            return jsonify({'error': 'Missing required fields'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Semester (semester_name, start_date, end_date) VALUES (%s, %s, %s)",
            (data['semester_name'], data['start_date'], data['end_date'])
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Semester added successfully'}), 201
    except:
        return jsonify({'error': 'Failed to add semester'}), 500

@app.route('/student_exam_system/view_semester', methods=['GET'])
def view_semester():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Semester")
        semesters = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({'semesters': semesters}), 200
    except:
        return jsonify({'error': 'Failed to retrieve semesters'}), 500

@app.route('/student_exam_system/update_semester/<int:semester_id>', methods=['PUT'])
def update_semester(semester_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE Semester SET semester_name = %s, start_date = %s, end_date = %s WHERE semester_id = %s",
        (data.get('semester_name'), data.get('start_date'), data.get('end_date'), semester_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Semester not found or no changes made'}), 404
    return jsonify({'message': 'Semester updated successfully'}), 200


@app.route('/student_exam_system/delete_semester/<int:semester_id>', methods=['DELETE'])
def delete_semester(semester_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Semester WHERE semester_id = %s", (semester_id,))
    
    conn.commit()
    row_count = cursor.rowcount
    cursor.close()
    conn.close()

    if row_count == 0:
        return jsonify({'error': 'Semester not found'}), 404
    return jsonify({'message': 'Semester deleted successfully'}), 200

@app.route('/student_exam_system/view_exam', methods=['GET'])
def view_exam():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Exam")
        exams = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({'exams': exams}), 200
    except:
        return jsonify({'error': 'Failed to retrieve exams'}), 500


@app.route('/student_exam_system/update_exam/<int:exam_id>', methods=['PUT'])
def update_exam(exam_id):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE Exam SET exam_date = %s, semester_id = %s WHERE exam_id = %s",
        (data.get('exam_date'), data.get('semester_id'), exam_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Exam not found or no changes made'}), 404
    return jsonify({'message': 'Exam updated successfully'}), 200

@app.route('/student_exam_system/delete_exam/<int:exam_id>', methods=['DELETE'])
def delete_exam(exam_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM Exam WHERE exam_id = %s", (exam_id,))
    
    conn.commit()
    row_count = cursor.rowcount
    cursor.close()
    conn.close()

    if row_count == 0:
        return jsonify({'error': 'Exam not found'}), 404
    return jsonify({'message': 'Exam deleted successfully'}), 200

@app.route('/student_exam_system/add_result_category', methods=['POST'])
def add_result_category():
    try:
        data = request.get_json()
        if not all(data.get(field) for field in ['category_code', 'mark_low', 'mark_high', 'description']):
            return jsonify({'error': 'Missing required fields'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO result_category (category_code, mark_low, mark_high, description) VALUES (%s, %s, %s, %s)",
            (data['category_code'], data['mark_low'], data['mark_high'], data['description'])
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Result category added successfully'}), 201
    except:
        return jsonify({'error': 'Failed to add result category'}), 500

@app.route('/student_exam_system/view_result_categories', methods=['GET'])
def view_result_categories():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM result_category")
        categories = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify({'result_categories': categories}), 200
    except:
        return jsonify({'error': 'Failed to retrieve result categories'}), 500

@app.route('/student_exam_system/update_result_category/<string:category_code>', methods=['PUT'])
def update_result_category(category_code):
    data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE result_category SET mark_low = %s, mark_high = %s, description = %s WHERE category_code = %s",
        (data.get('mark_low'), data.get('mark_high'), data.get('description'), category_code)
    )

    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Result category not found or no changes made'}), 404
    return jsonify({'message': 'Result category updated successfully'}), 200


@app.route('/student_exam_system/delete_result_category/<string:category_code>', methods=['DELETE'])
def delete_result_category(category_code):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM result_category WHERE category_code = %s", (category_code,))
    conn.commit()
    cursor.close()
    conn.close()

    if cursor.rowcount == 0:
        return jsonify({'error': 'Result category not found'}), 404
    return jsonify({'message': 'Result category deleted successfully'}), 200


@app.route('/student_exam_system/performance_summary/<int:student_id>', methods=['GET'])
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
            return jsonify({'error': 'No data found'}), 404

        grades = [float(r['grade']) for r in results]
        return jsonify({
            'exams': len(results),
            'average': sum(grades) / len(grades),
            'details': results
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/student_exam_system/exam-results/<int:student_id>', methods=['GET'])
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
        return jsonify({'error': 'No exam results found for this student'}), 404
    return jsonify(exam_results)


if __name__ == '__main__':
    app.run(debug=True)
