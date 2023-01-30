import sqlite3
db_location='school.db'
connection=sqlite3.connect(db_location)
cursor=connection.cursor()
query='''
    create table if not exists student(
        id int PRIMARY KEY,
        name text(100) not null,
        class text not null,
        marks int not null
    )
'''
cursor.execute(query)
connection.commit()
connection.close()