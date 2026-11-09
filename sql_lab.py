import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()

cur.executescript("""
CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE scores (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    subject TEXT,
    score INTEGER,
    FOREIGN KEY (student_id) REFERENCES students(id)
);
INSERT INTO students VALUES (1,'Ali','Cairo'), (2,'Sara','Giza'), (3,'Omar','Cairo'), (4,'Mona','Alex');
INSERT INTO scores VALUES (1,1,'ML',90), (2,1,'SQL',70), (3,2,'ML',85), (4,2,'SQL',95), (5,3,'ML',60);
""")

def show(title, sql):
    print("--", title)
    for row in cur.execute(sql):
        print(row)
    print()

show("1) all students", "SELECT * FROM students")
show("2) students in Cairo", "SELECT name FROM students WHERE city = 'Cairo'")
show("3) scores high to low", "SELECT subject, score FROM scores ORDER BY score DESC")
show("4) average per subject",
     "SELECT subject, COUNT(*), AVG(score) FROM scores GROUP BY subject")
show("5) INNER JOIN",
     "SELECT s.name, c.subject, c.score FROM students s JOIN scores c ON c.student_id = s.id")
show("6) LEFT JOIN",
     "SELECT s.name, c.subject, c.score FROM students s LEFT JOIN scores c ON c.student_id = s.id")
show("7) average per student, only above 80",
     "SELECT s.name, AVG(c.score) AS avg_score FROM students s JOIN scores c ON c.student_id = s.id GROUP BY s.name HAVING AVG(c.score) > 80")