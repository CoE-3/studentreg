import webapp2 
from google.appengine.ext import ndb
import jinja2
import os
import logging

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#CLASS FOR THE CREATE STUDENT DATABASE
class createstudent(ndb.Model):
    first_name = ndb.StringProperty(indexed=True)
    last_name = ndb.StringProperty(indexed=True)
    age = ndb.IntegerProperty()
    gender = ndb.StringProperty(indexed=True)
    date = ndb.DateTimeProperty(auto_now_add=True)

#CLASS FOR MAIN PAGE 
class MainPage(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('main_page.html')
		self.response.write(template.render())

#CLASS FOR CREATE STUDENT FORM
class CreateStudentform(webapp2.RequestHandler):
	def get(self):												
		template = JINJA_ENVIRONMENT.get_template('student_form.html')
		self.response.write(template.render())

	def post(self):	
		student = createstudent()								
		student.first_name = self.request.get('first_name')
		student.last_name = self.request.get('last_name')
		student.age = int(self.request.get('age'))
		student.gender = self.request.get('gender')
		a= student.put() #returns the key of the entity created
		self.redirect('/student/createsuccess')

class CreateSuccess(webapp2.RequestHandler):
	def get(self):
		template = JINJA_ENVIRONMENT.get_template('create_success.html')
		self.response.write(template.render())
		
class StudentList(webapp2.RequestHandler):
    def get(self):
        students = createstudent.query().order(-createstudent.date).fetch()
        logging.info(students)
        template_data = {
            'student_list': students
        }
        template = JINJA_ENVIRONMENT.get_template('student_list.html')
        self.response.write(template.render(template_data))

class ViewStudent(webapp2.RequestHandler):
	def get(self,student_id):
		studentdet = createstudent.query().order(-createstudent.date).fetch()
		stud_id = int(student_id)
		template_data = {
            'student_details': studentdet,
            'id': stud_id,
        }
		template = JINJA_ENVIRONMENT.get_template('student_view.html')
		self.response.write(template.render(template_data))

class EditStudent(webapp2.RequestHandler):
	def get(self,student_id):
		students = createstudent.get_by_id(int(student_id))
		template_data = {
            'student': students
        }
		template = JINJA_ENVIRONMENT.get_template('student_edit.html')
		self.response.write(template.render(template_data))

	def post(self,student_id):	
		students = createstudent.get_by_id(int(student_id))							
		students.first_name = self.request.get('first_edit')
		students.last_name = self.request.get('last_edit')
		students.age = int(self.request.get('age_edit'))
		students.gender = self.request.get('gender_edit')
		students.put() #returns the key of the entity created
		self.redirect('/student/editsuccess')

class EditSuccess(webapp2.RequestHandler):
	def get(self):												
		template = JINJA_ENVIRONMENT.get_template('edit_success.html')
		self.response.write(template.render())

class DeleteStudent(webapp2.RequestHandler):
  	def get(self,student_id):
  		student = createstudent.get_by_id(int(student_id))
  		student.key.delete()
  		self.redirect('/student/deletesuccess')

class DeleteSuccess(webapp2.RequestHandler):
	def get(self):												
		template = JINJA_ENVIRONMENT.get_template('delete_success.html')
		self.response.write(template.render)
		
app = webapp2.WSGIApplication([
	('/student/create',CreateStudentform),
	('/student/list',StudentList),
	('/student/delete/(.*)',DeleteStudent),
	('/student/edit/(.*)',EditStudent),
	('/student/deletesuccess',DeleteSuccess),
	('/student/createsuccess',CreateSuccess),
	('/student/editsuccess',EditSuccess),
	('/student/(.*)',ViewStudent),
	('/',MainPage)
],debug = True)