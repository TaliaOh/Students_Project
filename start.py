from flask import Flask, request, render_template
import psycopg2

from datetime import datetime

app = Flask(__name__)

# '/' route: returns a search form to search for students by name. 
# If a POST request is received, the code runs a SQL query to search for a student by name using a 
# search term received from the form. If a student is found, the search results are displayed in a template.
@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template('search_student.html')
    else:
        search_term = request.form.get('studentname')
        conn = psycopg2.connect(
            host="localhost",
            database="training",
            user="postgres",
            password="Talia7965528")
        c = conn.cursor()

        sql_string = """ 
                        SELECT name,studentid , address , gender , dob
                        FROM students WHERE name ILIKE %s
                    """
        search_term = "%"+search_term+"%"
        c.execute(sql_string, (search_term,))
        results = c.fetchall()
        # -----------SQL code above this line---------------------
        return render_template('search_results.html', mylist=results)

# returns a search form to search for student scores by ID. 
# If a POST request is received, the code runs a SQL query to search for
# a student by ID and displays the scores for the student in a template.
@app.route('/search_scores', methods=['GET', 'POST'])
def search_scores():
    if request.method == 'GET':
        return render_template('search_scores.html')
    else:
        search_term = request.form.get('studentid')
        search_term = int(search_term)

        conn = psycopg2.connect(
            host="localhost",
            database="training",
            user="postgres",
            password="Talia7965528")
        c = conn.cursor()

        sql_string = """ 
                        SELECT name,students.studentid , course_code , score
                        FROM 
                            students JOIN scores USING(studentid)
                        WHERE 
                            studentid =%s
                    """
        c.execute(sql_string, (search_term,))
        results = c.fetchall()
        conn.commit()
        c.close()
        conn.close()

        if len(results) == 0:
            return 'There is no one by that student ID'

        else:
            return render_template('score_results.html', mylist=results)

#  returns a form to add a student to the database. If a POST request is received, 
# the code adds a new student to the "students" 
# table and adds any scores for that student to the "scores" table.
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        return render_template('add_student.html')
    else:
        studentname = request.form.get('studentname')
        sid = request.form.get('id')
        address = request.form.get('address')
        gender = request.form.get('gender')
        dob = request.form.get('dob')
        chem101 = request.form.get('chem101')
        math101 = request.form.get('math101')
        phys101 = request.form.get('phys101')

        if not studentname or not sid:
            return "Name and StudentID are required"
        else:
            sid = int(sid)

        conn = psycopg2.connect(
            host="localhost",
            database="training",
            user="postgres",
            password="Talia7965528")
        c = conn.cursor()

        student = (studentname, sid, address, gender, dob)

        sql_string = """
                        INSERT INTO students(name , studentid , address , gender , dob)
                        VALUES 
                              (%s,%s,%s,%s, %s)    
                    """
        c.execute(sql_string, student)
        conn.commit()

        sql_string = """
                        INSERT INTO scores( studentid , course_code, score)
                        VALUES 
                              (%s,%s,%s)    
                     """
        if chem101:
            c.execute(sql_string, (sid, 'CHEM101', float(chem101)))
        if math101:
            c.execute(sql_string, (sid, 'MATH101', float(math101)))
        if phys101:
            c.execute(sql_string, (sid, 'PHYS101', float(phys101)))

        conn.commit()
        c.close()
        conn.close()

        return f"The student {studentname} was created....OK"

# returns a template displaying information about all courses stored in the "course_info" table.
@app.route('/courses')
def courses():
    # ------------Enter SQL code below--------------
    conn = psycopg2.connect(
        host="localhost",
        database="training",
        user="postgres",
        password="Talia7965528")
    c = conn.cursor()
    c.execute("""SELECT * FROM course_info""")

    all_data = c.fetchall()
    conn.commit()
    c.close()
    conn.close()

    # --------------------End SQL code ------------------------
    return render_template('course_info.html', course_details=all_data)
