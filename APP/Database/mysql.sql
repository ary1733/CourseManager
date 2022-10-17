CREATE TABLE Course
(
  Course_cd VARCHAR(255) NOT NULL,
  Course_name VARCHAR(255) NOT NULL,
  Semester INTEGER,
  Credits INTEGER,
  Instructor_Name VARCHAR(255) NOT NULL,
  PRIMARY KEY (Course_cd)
);

CREATE TABLE Student
(
  Roll_no VARCHAR(255) NOT NULL,
  Student_name VARCHAR(255) NOT NULL,
  Dept_Name VARCHAR(255) NOT NULL,
  Email_Id VARCHAR(255) NOT NULL,
  PRIMARY KEY (Roll_no)
);

CREATE TABLE Course_Student
(
  Course_cd VARCHAR(255) NOT NULL,
  Roll_no VARCHAR(255) NOT NULL,
  PRIMARY KEY (Course_cd, Roll_no),
  FOREIGN KEY (Course_cd) REFERENCES Course(Course_cd) ON DELETE CASCADE,
  FOREIGN KEY (Roll_no) REFERENCES Student(Roll_no) ON DELETE CASCADE
);
