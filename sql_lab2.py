import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()
cur.executescript("""
CREATE TABLE students (id INTEGER PRIMARY KEY, name TEXT, city TEXT);
CREATE TABLE scores (id INTEGER PRIMARY KEY, student_id INTEGER, subject TEXT, score INTEGER);
INSERT INTO students VALUES (1,'Ali','Cairo'), (2,'Sara','Giza'), (3,'Omar','Cairo'), (4,'Mona','Alex');
INSERT INTO scores VALUES (1,1,'ML',90), (2,1,'SQL',70), (3,2,'ML',85), (4,2,'SQL',95), (5,3,'ML',60);
""")

def show(title, sql, params=()):
    print("--", title)
    for row in cur.execute(sql, params):
        print(row)
    print()


cur.execute("UPDATE scores SET score = 65 WHERE id = 5")
cur.execute("INSERT INTO scores (student_id, subject, score) VALUES (?, ?, ?)", (4, "ML", 88))
cur.execute("DELETE FROM scores WHERE id = 2")
con.commit()
show("1) scores after changes", "SELECT * FROM scores")

user_input = "Cairo' OR '1'='1"
show("2a) f-string (UNSAFE)", f"SELECT name FROM students WHERE city = '{user_input}'")
show("2b) with ? (SAFE)", "SELECT name FROM students WHERE city = ?", (user_input,))


show("3) scores above the overall average",
     "SELECT student_id, score FROM scores WHERE score > (SELECT AVG(score) FROM scores)")


cur.execute("CREATE INDEX idx_scores_student ON scores(student_id)")
show("4) query plan", "EXPLAIN QUERY PLAN SELECT * FROM scores WHERE student_id = 2")