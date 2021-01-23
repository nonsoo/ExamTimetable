import sqlite3
from make_tables import check_courses


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


def get_course_instructors(db, course):
    '''Return the Course number, sections and instructors for the given
    course number.

    >>> get_course_instructors('exams.db', 'BIOC12H3F')
    [('BIOC12H3F', 'LEC01', 'R. Zhao')]

    >>> get_course_instructors('exams.db', 'BIOC15H3F')
    [('BIOC15H3F', 'LEC01', 'C. Hasenkampf')]

    >>> get_course_instructors('exams.db', 'CSCA20H3F')
    [('CSCA20H3F', 'ALL', 'A. Bretscher')]
    '''

    # From the given course code, its going to return the course code, section
    # number and instructors for the course
    query = '''SELECT Course, Section, Name FROM Courses
    WHERE Course= ?'''
    args = (course,)
    return run_query(db, query, args)


def get_course_time(db, course):
    '''Return the course number, ID, the date and start time of the given
    course's exam for all sections. Note there are only multiple sections if
    the course IDs are different.

    >>> get_course_time('exams.db', 'BIOC12H3F')
    [('BIOC12H3F', '32', '17-12-18', '14:00')]

    >>> get_course_time('exams.db', 'BIOC15H3F')
    [('BIOC15H3F', '33', '17-12-11', '9:00')]

    >>> get_course_time('exams.db', 'BIOC32H3F')
    [('BIOC32H3F', '35', '17-12-07', '19:00')]
    '''

    # From the given course, its going to return the course code, id, date
    # and start time for the course
    query = '''SELECT DISTINCT Courses.Course, Courses.ID, Time.Date,
    Time.Start FROM Courses JOIN Time ON Courses.ID = Time.ID WHERE
    Course = ? '''
    args = (course,)
    return run_query(db, query, args)


def get_course_time_section(db, course, section):
    '''Return the course number, section, the date and start time of the
    given course's exam.

    >>> get_course_time_section('exams.db', 'BIOC12H3F', 'LEC01')
    [('BIOC12H3F', 'LEC01', '17-12-18', '14:00')]

    >>> get_course_time_section('exams.db', 'BIOC15H3F', 'LEC01')
    [('BIOC15H3F', 'LEC01', '17-12-11', '9:00')]

    >>> get_course_time_section('exams.db', 'BIOC32H3F', 'LEC01')
    [('BIOC32H3F', 'LEC01', '17-12-07', '19:00')]
    '''

    # For the given course and section, the function is going to retrieve the
    # courseSection date, course code, and start time
    query = '''SELECT DISTINCT Courses.Course, Courses.Section, Time.Date,
    Time.Start FROM Courses JOIN Time ON Courses.ID = Time.ID WHERE
    Course = ? AND Section= ?'''
    args = (course, section)
    return run_query(db, query, args)


def courses_multi_instructors(db):
    '''Return the course number and instructor names for courses with more
    than one instructor. Note that this means the ID must be
    the same for each instructor.

    >>> courses_multi_instructors('exams.db')
    [('BIOA01H3F', 'M. Fitzpatrick'), ('BIOA01H3F', 'A. Ashok'),\
 ('BIOA01H3F', 'S. Brunt'), ('CHMA10H3F', 'S. Ballantyne'),\
 ('CHMA10H3F', 'N. Thavarajah'), ('CHMB16H3F', 'R. Soong'),\
 ('CHMB16H3F', 'K. Kerman'), ('CSCA08H3F', 'M. Ahmadzadeh'),\
 ('CSCA08H3F', 'B. Harrington'), ('CSCA67H3F', 'R. Pancer'),\
 ('CSCA67H3F', 'A. Bretscher'), ('HLTC16H3F', 'C. Furness'),\
 ('HLTC16H3F', 'E. Seto'), ('MATA29H3F', 'G. Scott'),\
 ('MATA29H3F', 'X. Jiang'), ('MATA32H3F', 'E. Moore'),\
 ('MATA32H3F', 'R. Grinnell'), ('MATA32H3F', 'R. Buchweitz'),\
 ('MATA67H3F', 'R. Pancer'), ('MATA67H3F', 'A. Bretscher'),\
 ('MGAB01H3F', 'L. Chen'), ('MGAB01H3F', 'G. Quan Fun'),\
 ('MGAB01H3F', 'L. Harvey'), ('MGAB03H3F', 'L. Chen'),\
 ('MGAB03H3F', 'G. Quan Fun'), ('MGAD65H3F', 'P. Phung'),\
 ('MGAD65H3F', 'S. Ratnam'), ('POLB80H3F', 'S. Pratt'),\
 ('POLB80H3F', 'C. LaRoche'), ('STAB22H3F', 'M. Soltanifar'),\
 ('STAB22H3F', 'N. Asidianya'), ('VPMA93H3F', 'B. Kingsbury'),\
 ('VPMA93H3F', 'R. King')]
    '''

    # The function is going to return only the course and instructor names
    # that have multiple instructors for one course
    query = '''SELECT Course, Name FROM Courses WHERE ID IN
    (SELECT ID FROM Courses GROUP BY ID having COUNT(*) > 1 )'''
    return run_query(db, query)


def courses_how_many_instructors(db):
    '''Return the course number and the number of instructors for courses with
    more than one instructor. Note that this means the ID must be
    the same for each instructor.

    >>> courses_how_many_instructors('exams.db')
    [('HLTC16H3F', 2), ('MATA29H3F', 2), ('MATA32H3F', 3), ('MATA67H3F', 2),\
 ('MGAB01H3F', 3), ('MGAB03H3F', 2), ('MGAD65H3F', 2), ('BIOA01H3F', 3),\
 ('POLB80H3F', 2), ('STAB22H3F', 2), ('VPMA93H3F', 2), ('CHMA10H3F', 2),\
 ('CHMB16H3F', 2), ('CSCA08H3F', 2), ('CSCA67H3F', 2)]
    '''

    # The function is going to return howmany instructors are assigned to each
    # course for courses that have multiple instructors
    query = '''SELECT DISTINCT Course, Count(ID) AS number_of_instructors
    FROM Courses GROUP BY ID HAVING COUNT (ID) > 1'''

    return run_query(db, query)


def find_dept_courses(db, dept):
    '''Return the courses from the given department.  Use  the "LIKE"
    clause in your SQL query for the course name.

    >>> find_dept_courses('exams.db', 'BIOA')
    [('BIOA01H3F',), ('BIOA11H3F',)]

    >>> find_dept_courses('exams.db', 'ANTA')
    [('ANTA01H3F',), ('ANTA02H3F',)]

    >>> find_dept_courses('exams.db', 'CSCA')
    [('CSCA08H3F',), ('CSCA20H3F',), ('CSCA67H3F',)]
    '''

    # The function is going to sort the courses based upon the courses that
    # possess similar names
    query = '''SELECT Distinct Course FROM Courses WHERE Course LIKE "'''\
        + str(dept) + '%"'
    return run_query(db, query)


def get_locations(db, course):
    '''Return the course, section and locations of the exam for the given
    course.

    >>> get_locations('exams.db', 'BIOC12H3F')
    [('BIOC12H3F', 'LEC01', 'SW319'), ('BIOC12H3F', 'LEC01', 'SY110')]


    >>> get_locations('exams.db', 'BIOC15H3F')
    [('BIOC15H3F', 'LEC01', 'SY110')]

    >>> get_locations('exams.db', 'BIOD23H3F')
    [('BIOD23H3F', 'LEC01', 'MW140')]
    '''

    # The function is going to return the course, section and location of the
    # exam for a given course
    query = '''SELECT DISTINCT Courses.Course, Courses.Section, Location.Room
    FROM Courses JOIN Location ON Courses.ID = Location.ID WHERE Course = ?'''
    args = (course,)
    return run_query(db, query, args)


def check_conflicts(db, course):
    '''Return  a list of course numbers of courses that  have conflicts with
    the given course.  A conflict is the same date and same start time.
    HINT: this may require more than one search.

    >>> check_conflicts('exams.db', 'BIOD23H3F')
    [('CSCD18H3F',), ('HLTB41H3F',), ('MGEA02H3F',),\
 ('MGEB11H3F',), ('MGEC40H3F',)]

    >>> check_conflicts('exams.db', 'BIOA01H3F')
    [('BIOB50H3F',), ('ENGB27H3F',), ('MGHB02H3F',), ('PHLB05H3F',)]

    >>> check_conflicts('exams.db', 'MGEC40H3F')
    [('BIOD23H3F',), ('CSCD18H3F',), ('HLTB41H3F',), ('MGEA02H3F',),\
 ('MGEB11H3F',)]
    '''
    query = '''SELECT DISTINCT Course FROM Courses JOIN Time ON
    Courses.ID = Time.ID WHERE Time.Date = ? AND Time.Start = ?
    AND Course != ?'''

    # Finds the start time and date for the course entered then searches the
    # database for other courses with the same start time and date
    conflict = get_course_time(db, course)
    args = (conflict[0][2], conflict[0][3], course)
    return run_query(db, query, args)


if __name__ == '__main__':
    # write your program here
    # you may assume the database has been made and has the name
    # DO NOT CHANGE THIS LINE
    db = 'exams.db'
    # add the rest of your code here
    my_course_lst = []
    valid_course = []
    exam_schedule = {}
    valid = check_courses(db)

    # Stores all courses for the semester in the lst 'valid_course' to allow
    # for validation later
    for i in range(len(valid)):
        valid_course.append(valid[i][1])

    # Asks the user to enter as many courses as they desire, until the user
    # returns nothing. Then converts all entered courses to uppercase to
    # prevent the program from crashing. Program then checks if the entered
    # course is a valid course. If the course entered is not a valid course,
    # then display Not a valid course
    quit = False
    while quit is False:
        entered_course = input('Please enter your course or return to quit: ')

        # Checks if course entered is a valid course
        if entered_course.upper() in valid_course:
            my_course_lst.append(entered_course.upper())
        elif entered_course == '':
            quit = True
        else:
            print('Not a valid course code, please re-enter or return to \
quit. ')

    # Retrieve Exam Times
    # Goes through every course in course lst and checks if the course has
    # multiple sections. If the course does not have multiple sections, then
    # retrive the exam time for the course. If the course has multiple
    # sections then retreive the exam time for the particular section of the
    # course. Then store the information in a dictionary where the key is the
    # specific course and the value is a list of tuple containing the exam
    # course_code, time, date, section/ID
    for course in my_course_lst:
        check_section = get_course_instructors(db, course)

        # CHECKS IF THE SECTION FOR THE PARTICULAR COURSE IS ALL
        if check_section[0][1] == 'ALL':
            exam_time = get_course_time(db, course)
        else:
            section = input('There are multiple sections of %s. What is your \
section?: ' % (course))
            exam_time = get_course_time_section(db, course, section.upper())
        # exam_schedule dict is dictionary containing course name as key and
        # course info as the value
        exam_schedule[course] = exam_time

    # Goes through keys and values in exam_schedule and prints the course with
    # time and date in accordance to the presence or absence of the section
    # If the course has a specific section then display the exam time for the
    # specific section of the course by checking if the first char for the
    # the item in course_info[0][1] is a digit or alph
    for (courses, course_info) in exam_schedule.items():
        if course_info[0][1][0].isdigit():
            print('Course %s has exam on %s at %s'
                  % (courses, course_info[0][2], course_info[0][3]))
        else:
            print('Course %s section %s has exam on %s at %s'
                  % (courses, course_info[0][1], course_info[0][2],
                     course_info[0][3]))
