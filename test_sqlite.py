import sqlite3


conn = sqlite3.connect("test.db")
cus = conn.cursor()
cus.execute("create table user(id varchar(20) primary key, name varchar(20))")
cus.execute("insert into user(id, name) values(1, '苏三')")
print(cus.rowcount)
cus.close()
conn.commit()
conn.close()
