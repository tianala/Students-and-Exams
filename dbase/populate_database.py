from faker import Faker
from random import randint, choice
import pymysql

# Set up Faker and database connection
faker = Faker()
conn = pymysql.connect(host='localhost', user='root', password='root', database='student_exam_system')
cursor = conn.cursor()

# Populate Result_Category Table
categories = [
    ('A', 90, 100, 'Excellent'),
    ('B', 80, 89, 'Good'),
    ('C', 70, 79, 'Average'),
    ('D', 60, 69, 'Below Average'),
    ('F', 0, 59, 'Fail')
]

for code, low, high, desc in categories:
    cursor.execute(
        "INSERT INTO Result_Category (category_code, mark_low, mark_high, description) VALUES (%s, %s, %s, %s)",
        (code, low, high, desc)
    )

# Populate Semester Table
semesters = [
('1st Semester',	'2024-08-12', '2024-12-17'),
('2nd Semester',	'2025-01-13',	'2025-05-23')
]

for name, start_date, end_date in semesters:
    cursor.execute(
        "INSERT INTO Semester (semester_name, start_date, end_date) VALUES (%s, %s, %s)",
        (name, start_date, end_date)
    )

# Populate Student Table
for _ in range(25):
    first_name = faker.first_name()
    last_name = faker.last_name()
    sex = randint(0, 1)  # 0 = Male, 1 = Female
    email = faker.email()
    cursor.execute(
        "INSERT INTO Student (first_name, last_name, sex, email) VALUES (%s, %s, %s, %s)",
        (first_name, last_name, sex, email)
    )

# Populate Exam Table
for _ in range(25):
    exam_date = faker.date_between(start_date='-1y', end_date='today')
    semester_id = randint(1, len(semesters))  # Randomly assign to an existing semester
    cursor.execute(
        "INSERT INTO Exam (exam_date, semester_id) VALUES (%s, %s)",
        (exam_date, semester_id)
    )

# Populate Exam_Result Table
for _ in range(25):
    student_id = randint(1, 25)  # Assume there are 25 students
    exam_id = randint(1, 25)  # Assume there are 25 exams
    grade = choice(['A', 'B', 'C', 'D', 'F'])
    cursor.execute(
        "INSERT INTO Exam_Result (student_id, exam_id, grade, category_code) VALUES (%s, %s, %s, %s)",
        (student_id, exam_id, grade, grade)  # Use grade as the category_code
    )

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Database populated successfully!")
