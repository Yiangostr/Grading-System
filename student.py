from google.appengine.ext import db

TABLE_NAME = "StudentDb"
PROPERTY_DICT = {'id':int, 'name':str, 'dob':str, 'class_name':str, 'year':int, 'quarter':str, 'mathematics':int, 'computer':int, 'litrature':int}
SUBJECT_LIST = ['mathematics', 'computer', 'litrature']

class StudentDb(db.Model):
    id = db.IntegerProperty(required=True)
    name = db.StringProperty(required=True)
    dob = db.DateProperty(required=True)
    class_name = db.StringProperty(required=True)
    year = db.IntegerProperty(required=True)
    quarter = db.StringProperty(required=True)
    mathematics = db.IntegerProperty(required=True)
    computer = db.IntegerProperty(required=True)
    litrature = db.IntegerProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)

def get_by_id(student_id):
    return StudentDb.get_by_id(int(student_id))

def get_by_student_id(student_id):
    return db.GqlQuery("SELECT * FROM StudentDb WHERE id = :1", student_id)

def get_by_name(student_name):
    return db.GqlQuery("SELECT * FROM StudentDb WHERE name = :1", student_name).get()

def get_all():
    return db.GqlQuery("SELECT * FROM StudentDb ORDER BY created DESC ")

def get_property_string():
    dic = PROPERTY_DICT.copy()
    return str(dic).replace('>', ']').replace('<', '[')