#import faceRe as fr
import mysql.connector as sql
conn = sql.connect(host="localhost",user='root',passwd='dh33raj1')
cur = conn.cursor()
cur.execute('use known_persons;')
cur.execute("""CREATE TABLE IF NOT EXISTS Person(unqID varchar(50) PRIMARY KEY);""")

def entry(obj):
    for i in obj:
        print(i)
        query = "insert into Person values();"
        cur.execute(query)
        conn.commit()
def unknown_entry(obj):

    length=len(obj)
    print(length)
    newId=str(2020010000+length)
    print(str(newId))
    query="Insert into Person values("+newId+");"
    print(query)
    cur.execute(query)
    conn.commit()
    return 1
def retrive():
    query="select * from Person;"
    cur.execute(query)
    li=cur.fetchall()
    lst=[]
    lst.clear()
    str(li)
    for i in li:
        lst.append(str(i[0]))
    print(lst)
    return lst
retrive()
#unknown_entry([1,2,3,4,5])
conn.commit()
