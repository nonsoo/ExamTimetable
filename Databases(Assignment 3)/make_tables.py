import csv
import sqlite3


# Create the tables
def create_location_table(db, loc_file):
    '''Location table has format ID, Room'''

    con = sqlite3.connect(db)
    cur = con. cursor()
    cur.execute('''DROP TABLE IF EXISTS Location''')
    # create the table
    cur.execute('''CREATE TABLE Location(ID TEXT, Room TEXT)''')

    # Add the rows
    loc_file.readline()
    reader = csv.reader(loc_file)
    for line in reader:
        # checks if then that is currently being read is empty:if so it is
        # going to skip. Then checks if the length of the line is greater than
        # 1. If line is greater than one, it suggests that there are multiple
        # rooms for that ID. It will then insert a room in the list of
        # multiple rooms on a separate row with the corresponding ID.
        # If the line is not greater than 1 then there is only one room
        # for that ID thus it will just insert course room with the
        # corresponding ID.
        if len(line) == 0:
            continue

        if len(line) > 1:
            i = 0
            while i < len(line[1:]):
                cur.execute('''INSERT INTO Location VALUES (?, ?)''',
                            (line[0], line[i+1]))
                i += 1
        else:
            cur.execute('''INSERT INTO Location VALUES (?, ?)''',
                        (line[0], line[1]))

    # commit and close cursor and connection
    con.commit()
    cur.close()
    con.close()


def create_course_table(db, course_file):
    '''Courses Table should be ID,Course,Section,First Initial Last Name'''

    con = sqlite3.connect(db)
    cur = con. cursor()

    cur.execute('''DROP TABLE IF EXISTS Courses''')
    # create the table
    cur.execute('''CREATE TABLE Courses (ID TEXT, Course TEXT, Section TEXT,
    Name TEXT)''')

    # Insert the rows
    course_file.readline()
    reader = csv.reader(course_file)
    for line in reader:
        # checks if then that is currently being read is empty:if so it is
        # going to skip. Then checks if the length of the line is greater than
        # 3. If line is greater than three, it suggests that there are
        # multiple instructors for that ID. It will then insert an instructor
        # in the list of multiple instructors on a separate row with the
        # corresponding ID. If the line is not greater than 3 then there is
        # only one instruc for that ID thus it will just insert course info
        # with the corresponding ID.
        if len(line) == 0:
            continue
        if len(line) > 3:
            i = 0
            while i < len(line[3:]):
                cur.execute('''INSERT INTO Courses VALUES (?, ?, ?, ?)''',
                            (line[0], line[1], line[2], line[i+3]))
                i += 1
        else:
            cur.execute('''INSERT INTO Courses VALUES (?, ?, ?, ?)''',
                        (line[0], line[1], line[2], line[3]))

    # commit and close the cursor and connection
    con.commit()
    cur.close()
    con.close()


def create_time_table(db, time_file):
    '''Time Table should be ID,Date,Start Time,End Time,Duration
    '''

    con = sqlite3.connect(db)
    cur = con. cursor()

    cur.execute('''DROP TABLE IF EXISTS Time''')

    # create the table
    cur.execute('''CREATE TABLE Time (ID TEXT, Date TEXT, Start TEXT,
    End TEXT, Duration TEXT)''')

    # insert the rows
    time_file.readline()
    reader = csv.reader(time_file)
    for line in reader:
        # If the currently is empty( length of the line is 0) then skip the
        # line and go onto the next line in the reader.
        if len(line) == 0:
            continue
        cur.execute('''INSERT INTO Time VALUES (?, ?, ?, ?, ?)''',
                    (line[0], line[1], line[2], line[3], line[4]))

    # commit and close the cursor and connection
    con.commit()
    cur.close()
    con.close()


def run_query(db, query, args=None):
    """(str, str, tuple) -> list of tuple
    Return the results of running query q with arguments args on
    database db."""

    conn = sqlite3.connect(db)
    cur = conn.cursor()
    # execute the query with the given args passed
    # if args is None, we have only a query
    if args is None:
        cur.execute(query)
    else:
        cur.execute(query, args)

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results


def check_courses(db):
    '''Return the entire Courses table'''
    return run_query(db, '''SELECT * FROM Courses''')


def check_time(db):
    '''Return the entire Time table '''

    return run_query(db, '''SELECT * FROM Time''')


def check_rooms(db):
    '''Return the entire Locations table '''

    return run_query(db, '''SELECT * FROM Location''')


if __name__ == '__main__':
    db = 'exams.db'
    # open the necessary files
    # Open all necessary files for use to create and populate the table
    location = open('locations.csv', 'r')
    course = open('courses.csv', 'r')
    time = open('time.csv', 'r')

    # create the tables
    create_location_table(db, location)
    create_course_table(db, course)
    create_time_table(db, time)

    # close the files
    location.close()
    course.close()
    time.close()
