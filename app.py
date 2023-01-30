from flask import Flask,render_template,request,redirect
from flask_restful import Api
from student import AllStudent,Student
import sqlite3
app=Flask(__name__)
api=Api(app)
api.add_resource(AllStudent,'/students')
api.add_resource(Student,'/student/<int:id>')
db_location='school.db'
def get_all_records():
    connection=sqlite3.connect(db_location)
    cursor=connection.cursor()
    query='select * from student'        
    results=cursor.execute(query)
    students=[]
    for result in results:
            students.append({
                'id':result[0],
                'name':result[1],
                'class':result[2],
                'marks':result[3]
            })
    connection.commit()
    connection.close()
    return students
def get_student(id):
    connection=sqlite3.connect(db_location)
    cursor=connection.cursor()
    query='select * from student where id=?'        
    results=cursor.execute(query,(id,))
    student=[]
    for result in results:
            student.append({
                'id':result[0],
                'name':result[1],
                'class':result[2],
                'marks':result[3]
            })
    connection.commit()
    connection.close()
    return student
@app.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        rollno=request.form['rollno']
        name=request.form['name']
        clas=request.form['class']
        marks=request.form['marks']
        connection=sqlite3.connect(db_location)
        cursor=connection.cursor()
        query='insert into student values (?,?,?,?)'
        cursor.execute(query,(rollno,name,clas,marks))
        connection.commit()
        connection.close()
    records=get_all_records()
    return render_template('index.html',records=records)
@app.route('/delete/<int:id>')
def delete(id):
    connection=sqlite3.connect(db_location)
    cursor=connection.cursor()
    query='delete from student where id=?'
    cursor.execute(query,(id,))
    connection.commit()
    connection.close()
    return redirect('/')
@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
    if request.method=='POST':
        name=request.form['name']
        clas=request.form['class']
        marks=request.form['marks']
        connection=sqlite3.connect(db_location)
        cursor=connection.cursor()
        query='update student set name=? , class=? , marks=? where id=?'
        cursor.execute(query,(name,clas,marks,id))
        connection.commit()
        connection.close()
        return redirect('/')
    student=get_student(id)
    return render_template('update.html',student=student[0])
    
if __name__=='__main__':
    app.run(debug=True)