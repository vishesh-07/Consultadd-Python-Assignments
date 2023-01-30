import sqlite3
from flask_restful import Resource,reqparse
from flask import jsonify
db_location='school.db'
parser=reqparse.RequestParser()
parser.add_argument('name',type=str,required=True,help='Please enter name of the student.')
parser.add_argument('class',type=str,required=True,help='Please enter class of the student.')
parser.add_argument('marks',type=int,required=True,help='Please enter marks of the student.')
update_parser=reqparse.RequestParser()
update_parser.add_argument('name',type=str)
update_parser.add_argument('class',type=str)
update_parser.add_argument('marks',type=int)
class Student(Resource):
    @classmethod
    def find_by_id(cls,id):
        connection=sqlite3.connect(db_location)
        cursor=connection.cursor()
        query='select * from student where id=?'
        result=cursor.execute(query,(id,))
        row=result.fetchone()
        if row:
            return row
        return None
    @classmethod
    def insert_student(cls,id,student):
        connection=sqlite3.connect(db_location)
        cursor=connection.cursor()
        query='insert into student values(?,?,?,?)'
        cursor.execute(query,(id,student['name'],student['class'],student['marks']))
        connection.commit()
        connection.close()
    @classmethod
    def update_student(cls,id,toUpdate,value):
        connection=sqlite3.connect(db_location)
        cursor=connection.cursor()
        query='update student set {}=? where id=?'.format(toUpdate)
        cursor.execute(query,(value,id))
        connection.commit()
        connection.close()
        # print(query)
    @classmethod
    def delete_student(cls,id):
        connection=sqlite3.connect(db_location)
        cursor=connection.cursor()
        query='delete from student where id=?'
        cursor.execute(query,(id,))
        connection.commit()
        connection.close()
    def get(self,id):
        student=Student.find_by_id(id)
        if(student):
            response={
                'id':student[0],
                'name':student[1],
                'class':student[2],
                'marks':student[3]
            }
            return response,200
        else:
            return {'message':'No Student Found'},404
    def post(self,id):
        if Student.find_by_id(id):
            return {'message':'A student with roll number {} already exists.'.format(id)},400
        data=parser.parse_args()
        print(data)
        # print(record)
        try:
            Student.insert_student(id,data)
        except:
            return {'message':'Error occured.'},500
        record={
            'id':id,
            'name':data['name'],
            'class':data['class'],
            'marks':data['marks']
        }
        return record,201
    def put(self,id):
        data=update_parser.parse_args()
        student=Student.find_by_id(id)
        if student is None:
            return {'message':'No Student Found'},404
        else:
            if(data['name']):
                updated_student={
                    id:id,
                    'name':data['name']
                }
                Student.update_student(id,'name',data['name'])
            if(data['class']):
                updated_student={
                    id:id,
                    'class':data['class']
                }
                Student.update_student(id,'class',data['class'])
            if(data['marks']):
                updated_student={
                    id:id,
                    'marks':data['marks']
                }
                Student.update_student(id,'marks',data['marks'])
            student=Student.find_by_id(id)
            data=[{
                'id':student[0],
                'name':student[1],
                'class':student[2],
                'marks':student[3]
            }]
            return data,200
    def delete(self,id):
        student=Student.find_by_id(id)
        if student is None:
            return {'message':'No Student Found'},404
        else:
            Student.delete_student(id)
            return {'message':'Student with id {} deleted successfully.'.format(id)}
class AllStudent(Resource):
    def get(self):
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
        return students,200
        
        