import sqlite3


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


def check_conflict(db, courseA, courseB):
    query = '''SELECT DISTINCT Date, Start FROM Time JOIN Courses ON
    Time.ID = Courses.ID WHERE Course = ?'''
    args1 = (courseA,)
    args2 = (courseB,)

    process1 = run_query(db, query, args1)
    process2 = run_query(db, query, args2)
    if process1[0][0] == process2[0][0] and process1[0][1] == process2[0][1]:
        return True
    return False




if __name__ == '__main__':
    db = 'exams.db'
    check = False
    my_lst = []
    #print(check_conflict(db, 'ANTC80H3F', 'BIOC12H3F'))

    while check is False:
        course = input('please enter a course: ')
        if course == '':
            check = True
        else:
            my_lst.append(course.upper())

    new_L = []
    for i in range(len(my_lst)):
        nextt = my_lst[i+1:]
        for j in range(len(nextt)):
            if check_conflict(db, my_lst[i], nextt[j]) is True:
                new_L.append([my_lst[i],nextt[j]])

    if len(new_L) != 0:
        for L in range(len(new_L)):
            print('Course %s and Course %s have a conflict' %(new_L[L][0],
                                                               new_L[L][1]))
    else:
        print('Your courses are conflict free')


# ANTC80H3F, BIOC12H3F, FREC54H3F