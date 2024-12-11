import pytest
from flask import Flask, jsonify, request
from unittest.mock import patch, MagicMock
from werkzeug.exceptions import HTTPException
from app import app, get_db_connection 

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DB_HOST'] = 'localhost'
    app.config['DB_USER'] = 'root'
    app.config['DB_PASSWORD'] = 'root'
    app.config['DB_NAME'] = 'student_exam_system'
    return app.test_client()

@patch('mysql.connector.connect')
def test_add_student_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    response = client.post('/student_exam_system/add_student', json={
        'first_name': 'John', 'last_name': 'Doe', 'sex': 'M', 'email': 'john.doe@example.com'
    })
    
    assert response.status_code == 201
    assert response.json == {'message': 'Student added successfully'}

@patch('mysql.connector.connect')
def test_add_student_missing_fields(mock_connect, client):
    response = client.post('/student_exam_system/add_student', json={
        'first_name': 'John', 'last_name': 'Doe'
    })
    
    assert response.status_code == 400
    assert response.json == {'error': 'Missing required fields'}

@patch('mysql.connector.connect')
def test_add_semester_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    response = client.post('/student_exam_system/add_semester', json={
        'semester_name': 'Fall 2024', 'start_date': '2024-09-01', 'end_date': '2024-12-15'
    })
    
    assert response.status_code == 201
    assert response.json == {'message': 'Semester added successfully'}

@patch('mysql.connector.connect')
def test_add_semester_missing_fields(mock_connect, client):
    response = client.post('/student_exam_system/add_semester', json={
        'semester_name': 'Fall 2024', 'start_date': '2024-09-01'
    })
    
    assert response.status_code == 400
    assert response.json == {'error': 'Missing required fields'}


@patch('mysql.connector.connect')
def test_add_exam_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    response = client.post('/student_exam_system/add_exam', json={
        'exam_date': '2024-10-15', 'semester_id': 1
    })
    
    assert response.status_code == 201
    assert response.json == {'message': 'Exam added successfully'}

@patch('mysql.connector.connect')
def test_add_exam_missing_fields(mock_connect, client):
    response = client.post('/student_exam_system/add_exam', json={
        'exam_date': '2024-10-15'
    })
    
    assert response.status_code == 400
    assert response.json == {'error': 'Missing required fields'}

@patch('mysql.connector.connect')
def test_add_result_category_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    
    response = client.post('/student_exam_system/add_result_category', json={
        'category_code': 'A', 'mark_low': 0, 'mark_high': 50, 'description': 'Fail'
    })
    
    assert response.status_code == 201
    assert response.json == {'message': 'Result category added successfully'}

@patch('mysql.connector.connect')
def test_add_result_category_missing_fields(mock_connect, client):
    response = client.post('/student_exam_system/add_result_category', json={
        'category_code': 'A', 'mark_low': 0
    })
    
    assert response.status_code == 400
    assert response.json == {'error': 'Missing field: mark_high'}

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['DB_HOST'] = 'localhost'
    app.config['DB_USER'] = 'root'
    app.config['DB_PASSWORD'] = 'root'
    app.config['DB_NAME'] = 'student_exam_system'
    return app.test_client()

@patch('mysql.connector.connect')
def test_view_all_students_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{'student_id': 1, 'first_name': 'John', 'last_name': 'Doe'}]
    
    response = client.get('/student_exam_system/all_students')
    
    assert response.status_code == 200
    assert response.json == [{'student_id': 1, 'first_name': 'John', 'last_name': 'Doe'}]

@patch('mysql.connector.connect')
def test_view_all_students_no_data(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    
    response = client.get('/student_exam_system/all_students')
    
    assert response.status_code == 404
    assert response.json == {'error': 'No students found'}

@patch('mysql.connector.connect')
def test_view_student_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {'student_id': 1, 'first_name': 'John', 'last_name': 'Doe'}
    
    response = client.get('/student_exam_system/student/1')
    
    assert response.status_code == 200
    assert response.json == {'student_id': 1, 'first_name': 'John', 'last_name': 'Doe'}

@patch('mysql.connector.connect')
def test_view_student_not_found(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    
    response = client.get('/student_exam_system/student/999')
    
    assert response.status_code == 404
    assert response.json == {'error': 'Student not found'}

@patch('mysql.connector.connect')
def test_view_semester_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{'semester_id': 1, 'semester_name': 'Fall 2024'}]
    
    response = client.get('/student_exam_system/view_semester')
    
    assert response.status_code == 200
    assert response.json == {'semesters': [{'semester_id': 1, 'semester_name': 'Fall 2024'}]}

@patch('mysql.connector.connect')
def test_view_semester_failure(mock_connect, client):
    mock_connect.side_effect = Exception("Failed to connect to the database")
    
    response = client.get('/student_exam_system/view_semester')
    
    assert response.status_code == 500
    assert response.json == {'error': 'Failed to retrieve semesters'}

@patch('mysql.connector.connect')
def test_view_exam_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{'exam_id': 1, 'exam_date': '2024-10-15'}]
    
    response = client.get('/student_exam_system/view_exam')
    
    assert response.status_code == 200
    assert response.json == {'exams': [{'exam_id': 1, 'exam_date': '2024-10-15'}]}

@patch('mysql.connector.connect')
def test_view_exam_failure(mock_connect, client):
    mock_connect.side_effect = Exception("Failed to connect to the database")
    
    response = client.get('/student_exam_system/view_exam')
    
    assert response.status_code == 500
    assert response.json == {'error': 'Failed to retrieve exams'}

@patch('mysql.connector.connect')
def test_view_result_categories_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{'category_id': 1, 'category_code': 'A'}]
    
    response = client.get('/student_exam_system/view_result_categories')
    
    assert response.status_code == 200
    assert response.json == {'result_categories': [{'category_id': 1, 'category_code': 'A'}]}

@patch('mysql.connector.connect')
def test_view_result_categories_failure(mock_connect, client):
    mock_connect.side_effect = Exception("Failed to connect to the database")
    
    response = client.get('/student_exam_system/view_result_categories')
    
    assert response.status_code == 500
    assert response.json == {'error': 'Failed to retrieve result categories'}

# Edge case testing for database connectivity
def test_get_db_connection_error():
    with patch('mysql.connector.connect', side_effect=Exception('Connection error')):
        with app.app_context():
            try:
                get_db_connection()
            except Exception as e:
                assert str(e) == 'Connection error'


@patch('mysql.connector.connect')
def test_update_student_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    data = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'sex': 'F',
        'email': 'jane.doe@example.com'
    }
    
    response = client.put('/student_exam_system/update_student/1', json=data)
    
    assert response.status_code == 200
    assert response.json == {'message': 'Student updated successfully'}

@patch('mysql.connector.connect')
def test_update_student_missing_fields(mock_connect, client):
    data = {
        'first_name': 'Jane',
        'last_name': 'Doe'
    }
    
    response = client.put('/student_exam_system/update_student/1', json=data)
    
    assert response.status_code == 400
    assert response.json == {'error': 'Missing required fields'}

@patch('mysql.connector.connect')
def test_update_student_not_found(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    
    data = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'sex': 'F',
        'email': 'jane.doe@example.com'
    }
    
    response = client.put('/student_exam_system/update_student/999', json=data)
    
    assert response.status_code == 404
    assert response.json == {'error': 'Student not found'}

@patch('mysql.connector.connect')
def test_update_semester_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    data = {
        'semester_name': 'Spring 2025',
        'start_date': '2025-01-15',
        'end_date': '2025-05-15'
    }
    
    response = client.put('/student_exam_system/update_semester/1', json=data)
    
    assert response.status_code == 200
    assert response.json == {'message': 'Semester updated successfully'}

@patch('mysql.connector.connect')
def test_update_semester_not_found(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    
    data = {
        'semester_name': 'Spring 2025',
        'start_date': '2025-01-15',
        'end_date': '2025-05-15'
    }
    
    response = client.put('/student_exam_system/update_semester/999', json=data)
    
    assert response.status_code == 404
    assert response.json == {'error': 'Semester not found or no changes made'}

@patch('mysql.connector.connect')
def test_update_exam_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    data = {
        'exam_date': '2025-01-25',
        'semester_id': 2
    }
    
    response = client.put('/student_exam_system/update_exam/1', json=data)
    
    assert response.status_code == 200
    assert response.json == {'message': 'Exam updated successfully'}

@patch('mysql.connector.connect')
def test_update_exam_not_found(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    
    data = {
        'exam_date': '2025-01-25',
        'semester_id': 2
    }
    
    response = client.put('/student_exam_system/update_exam/999', json=data)
    
    assert response.status_code == 404
    assert response.json == {'error': 'Exam not found or no changes made'}

@patch('mysql.connector.connect')
def test_update_result_category_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    data = {
        'mark_low': 50,
        'mark_high': 60,
        'description': 'Pass'
    }
    
    response = client.put('/student_exam_system/update_result_category/A', json=data)
    
    assert response.status_code == 200
    assert response.json == {'message': 'Result category updated successfully'}

@patch('mysql.connector.connect')
def test_update_result_category_not_found(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    
    data = {
        'mark_low': 50,
        'mark_high': 60,
        'description': 'Pass'
    }
    
    response = client.put('/student_exam_system/update_result_category/B', json=data)
    
    assert response.status_code == 404
    assert response.json == {'error': 'Result category not found or no changes made'}

@patch('mysql.connector.connect')
def test_delete_student_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    response = client.delete('/student_exam_system/delete_student/1')
    
    assert response.status_code == 200
    assert response.json == {'message': 'Student deleted successfully'}

@patch('mysql.connector.connect')
def test_delete_student_not_found(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    
    response = client.delete('/student_exam_system/delete_student/999')
    
    assert response.status_code == 404
    assert response.json == {'error': 'Student not found'}

@patch('mysql.connector.connect')
def test_delete_semester_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    response = client.delete('/student_exam_system/delete_semester/1')
    
    assert response.status_code == 200
    assert response.json == {'message': 'Semester deleted successfully'}

@patch('mysql.connector.connect')
def test_delete_semester_not_found(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    
    response = client.delete('/student_exam_system/delete_semester/999')
    
    assert response.status_code == 404
    assert response.json == {'error': 'Semester not found'}

@patch('mysql.connector.connect')
def test_delete_exam_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    response = client.delete('/student_exam_system/delete_exam/1')
    
    assert response.status_code == 200
    assert response.json == {'message': 'Exam deleted successfully'}

@patch('mysql.connector.connect')
def test_delete_exam_not_found(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    
    response = client.delete('/student_exam_system/delete_exam/999')
    
    assert response.status_code == 404
    assert response.json == {'error': 'Exam not found'}

@patch('mysql.connector.connect')
def test_delete_result_category_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 1
    
    response = client.delete('/student_exam_system/delete_result_category/A')
    
    assert response.status_code == 200
    assert response.json == {'message': 'Result category deleted successfully'}

@patch('mysql.connector.connect')
def test_delete_result_category_not_found(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 0
    
    response = client.delete('/student_exam_system/delete_result_category/B')
    
    assert response.status_code == 404
    assert response.json == {'error': 'Result category not found'}

@patch('mysql.connector.connect')
def test_performance_summary_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {'exam_id': 1, 'exam_date': '2024-12-01', 'grade': 85.0, 'description': 'Pass'},
        {'exam_id': 2, 'exam_date': '2024-12-02', 'grade': 75.0, 'description': 'Fail'}
    ]
    
    response = client.get('/student_exam_system/performance_summary/1')
    
    assert response.status_code == 200
    assert response.json['exams'] == 2
    assert response.json['average'] == 80.0

@patch('mysql.connector.connect')
def test_performance_summary_no_data(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    
    response = client.get('/student_exam_system/performance_summary/999')
    
    assert response.status_code == 404
    assert response.json == {'error': 'No data found'}

@patch('mysql.connector.connect')
def test_view_exam_results_success(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [
        {
            'student_id': 1, 'first_name': 'John', 'last_name': 'Doe', 'sex': 'M', 'email': 'john.doe@example.com', 
            'exam_id': 1, 'exam_date': '2024-12-01', 'semester_id': 1, 'result_id': 1, 'grade': 85.0, 'result_category': 'Pass'
        },
        {
            'student_id': 1, 'first_name': 'John', 'last_name': 'Doe', 'sex': 'M', 'email': 'john.doe@example.com', 
            'exam_id': 2, 'exam_date': '2024-12-02', 'semester_id': 1, 'result_id': 2, 'grade': 75.0, 'result_category': 'Fail'
        }
    ]
    
    response = client.get('/student_exam_system/exam-results/1')
    
    assert response.status_code == 200
    assert len(response.json) == 2

@patch('mysql.connector.connect')
def test_view_exam_results_no_data(mock_connect, client):
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = []
    
    response = client.get('/student_exam_system/exam-results/999')
    
    assert response.status_code == 404
    assert response.json == {'error': 'No exam results found for this student'}
