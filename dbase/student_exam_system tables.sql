create database student_exam_system;
use student_exam_system;

CREATE TABLE Student (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
	sex tinyint,
    email VARCHAR(100));
    
CREATE TABLE Semester (
    semester_id INT AUTO_INCREMENT PRIMARY KEY,
    semester_name VARCHAR(50),
    start_date DATE,
    end_date DATE
);

CREATE TABLE Exam (
    exam_id INT AUTO_INCREMENT PRIMARY KEY,
    exam_date DATE,
    semester_id INT,
    FOREIGN KEY (semester_id) REFERENCES Semester(semester_id)
);
-- Update Exam Result Table
CREATE TABLE Exam_Result (
    result_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT,
    exam_id INT,
    grade VARCHAR(5),
    category_code VARCHAR(10),
    FOREIGN KEY (student_id) REFERENCES Student(student_id),
    FOREIGN KEY (exam_id) REFERENCES Exam(exam_id),
    FOREIGN KEY (category_code) REFERENCES Result_Category(category_code)
);

-- Create Result Category Table
CREATE TABLE Result_Category (
    category_code VARCHAR(10) PRIMARY KEY,
    mark_low INT,
    mark_high INT,
    description VARCHAR(100)
);

