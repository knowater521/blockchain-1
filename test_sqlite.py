import sqlite3


conn = sqlite3.connect("test.db")
cus = conn.cursor()
# cus.execute("insert into blockchain('index', block) values(1, '苏三')")
# cus.execute("insert into blockchain('index', block) values(2, '救死扶伤'), (3, '温热无'), (4, '放松放松')")
cus.execute("insert into blockchain values(3, '搞事')")
task = cus.execute("select block from blockchain where \"index\"=1")
# task = cus.execute("select count(*)  from sqlite_master where type='table' and name = 'blockchain'")
print(task.fetchone())
cus.close()
conn.commit()
conn.close()
