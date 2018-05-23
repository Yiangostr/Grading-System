import os
import webapp2
import cgi
import json
import logging
import datetime
import collections

import student

STATUS_KEY = 'status'
DESC_KEY = 'description'

STATUS_ERROR = 'error'
STATUS_OK = 'ok'

REPLY_DICT = {STATUS_KEY: "", DESC_KEY: ""}

class Default(webapp2.RequestHandler):
	def get(self):
		dict = {'required_properties': student.get_property_string(), 'method': 'POST'}
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(dict))

class SubjectQuaterAnalysis(webapp2.RequestHandler):
	def get(self):
		students = student.get_all()
		subject_dict = {'mathematics':0, 'computer':0, 'litrature':0}
		output_list = {'Q1':subject_dict.copy(),'Q2':subject_dict.copy(),'Q3':subject_dict.copy(),'Q4':subject_dict.copy()}
		total = {'Q1':float(0),'Q2':float(0),'Q3':float(0),'Q4':float(0)}
		for data in students:
			q = data.quarter
			output_list[q]['mathematics'] += float(data.mathematics)
			output_list[q]['computer'] += float(data.computer)
			output_list[q]['litrature'] += float(data.litrature)
			total[q] += float(1)
		
		for i in total.keys():
			if total[i] == 0:
				total[i] += 1
		output_list['Q1']['mathematics'] = float(output_list['Q1']['mathematics'])/total['Q1']
		output_list['Q1']['computer'] = float(output_list['Q1']['computer'])/total['Q1']
		output_list['Q1']['litrature'] = float(output_list['Q1']['litrature'])/total['Q1']
		output_list['Q2']['mathematics'] = float(output_list['Q2']['mathematics'])/total['Q2']
		output_list['Q2']['computer'] = float(output_list['Q2']['computer'])/total['Q2']
		output_list['Q2']['litrature'] = float(output_list['Q2']['litrature'])/total['Q2']
		output_list['Q3']['mathematics'] = float(output_list['Q3']['mathematics'])/total['Q3']
		output_list['Q3']['computer'] = float(output_list['Q3']['computer'])/total['Q3']
		output_list['Q3']['litrature'] = float(output_list['Q3']['litrature'])/total['Q3']
		output_list['Q4']['mathematics'] = float(output_list['Q4']['mathematics'])/total['Q4']
		output_list['Q4']['computer'] = float(output_list['Q4']['computer'])/total['Q4']
		output_list['Q4']['litrature'] = float(output_list['Q4']['litrature'])/total['Q4']

		REPLY_DICT[STATUS_KEY] = STATUS_OK
		REPLY_DICT[DESC_KEY] = output_list
		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(REPLY_DICT))

class SubjectAnalysis(webapp2.RequestHandler):
	def get(self, subject):
		print "subject: ", subject
		subject_index = int(subject)
		if subject_index in range(len(student.SUBJECT_LIST)):
			students = student.get_all()
			output_list = {'Q1':float(0),'Q2':float(0),'Q3':float(0),'Q4':float(0)}
			total = {'Q1':float(0),'Q2':float(0),'Q3':float(0),'Q4':float(0)}
			for data in students:
				value = 0
				if subject_index == 0:
					value = data.mathematics
				elif subject_index == 1:
					value = data.computer
				elif subject_index == 2:
					value = data.litrature

				q = data.quarter
				output_list[q] += float(value)
				total[q] += float(1)

			for i in total.keys():
				if total[i] == 0:
					total[i] += float(1)
				output_list[i] = output_list[i]/total[i]


			REPLY_DICT[STATUS_KEY] = STATUS_OK
			REPLY_DICT[DESC_KEY] = output_list
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(REPLY_DICT))
		else:
			REPLY_DICT[STATUS_KEY] = STATUS_ERROR
			REPLY_DICT[DESC_KEY] = "The subject does not exist " + str(student.SUBJECT_LIST) + " == " + str(range(len(student.SUBJECT_LIST))) 
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(REPLY_DICT))

class QuaterAnalysis(webapp2.RequestHandler):
	def get(self, student_id):
		print student_id
		data = student.get_by_student_id(int(student_id))
		dic_list = []
		if data:
			if isinstance(data, collections.Iterable):
				for da in data:
					dic = {}
					dic['id'] = da.id
					dic['name'] = da.name
					dic['dob'] = str(da.dob)
					dic['class_name'] = da.class_name
					dic['year'] = da.year
					dic['quarter'] = da.quarter
					dic['mathematics'] = da.mathematics
					dic['litrature'] = da.litrature
					dic['computer'] = da.computer
					dic_list.append(dic)	
			else:
				dic = {}
				dic['id'] = data.id
				dic['name'] = data.name
				dic['dob'] = str(data.dob)
				dic['class_name'] = data.class_name
				dic['year'] = data.year
				dic['quarter'] = data.quarter
				dic['mathematics'] = data.mathematics
				dic['litrature'] = data.litrature
				dic['computer'] = data.computer
				dic_list.append(dic)

		output_list = {'Q1':float(0),'Q2':float(0),'Q3':float(0),'Q4':float(0)}
		total_quarter = len(dic_list)
		if total_quarter > 0:
			for q in dic_list:
				quart = q['quarter']
				output_list[quart] = (float(q['mathematics'])+float(q['computer'])+float(q['litrature'])) / float(3)
			REPLY_DICT[STATUS_KEY] = STATUS_OK
			REPLY_DICT[DESC_KEY] = output_list
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(REPLY_DICT))
		else:
			REPLY_DICT[STATUS_KEY] = STATUS_ERROR
			REPLY_DICT[DESC_KEY] = "Insufficient Data"
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(REPLY_DICT))


class SingleStudent(webapp2.RequestHandler):
	def get(self, student_id):
		print student_id
		data = student.get_by_student_id(int(student_id))
		if data:
			dic_list = []
			if isinstance(data, collections.Iterable):
				for da in data:
					dic = {}
					dic['id'] = da.id
					dic['name'] = da.name
					dic['dob'] = str(da.dob)
					dic['class_name'] = da.class_name
					dic['year'] = da.year
					dic['quarter'] = da.quarter
					dic['mathematics'] = da.mathematics
					dic['litrature'] = da.litrature
					dic['computer'] = da.computer
					dic_list.append(dic)	
			else:
				dic = {}
				dic['id'] = data.id
				dic['name'] = data.name
				dic['dob'] = str(data.dob)
				dic['class_name'] = data.class_name
				dic['year'] = data.year
				dic['quarter'] = data.quarter
				dic['mathematics'] = data.mathematics
				dic['litrature'] = data.litrature
				dic['computer'] = data.computer
				dic_list.append(dic)

			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(dic_list))
		else:
			REPLY_DICT[STATUS_KEY] = STATUS_ERROR
			REPLY_DICT[DESC_KEY] = "Student ID Not Found"
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(REPLY_DICT))


class SubmitStudent(webapp2.RequestHandler):

	def format_date(self, date):
		datesp = date.split('-')
		for i in range(len(datesp)):
			d = datesp[i]
			if len(d) < 2:
				datesp[i] = "0" + datesp[i]
		new_date = str(datesp[2]) + str(datesp[1]) + str(datesp[0])
		return new_date

	def check_date(self, date):
		return len(date) == 8

	def check_quarter(self,q):
		if len(q) == 2 and q[0] == 'Q' and q[1].isdigit() and int(q[1]) > 0 and int(q[1]) < 5:
			return True
		else:
			return False

	def create_student(self, data):
		st = student.StudentDb(
			id = data['id'], 
			name = data['name'],
			dob = data['dob'],
			class_name = data['class_name'],
			year = data['year'],
			quarter = data['quarter'],
			mathematics = data['mathematics'],
			computer = data['computer'],
			litrature = data['litrature']
		 )
		st.put()
		return st.key().id()

	def get(self):
		students = student.get_all()
		output_list = []
		for data in students:
			dic = {}
			dic['id'] = data.id
			dic['name'] = data.name
			dic['dob'] = str(data.dob)
			dic['class_name'] = data.class_name
			dic['year'] = data.year
			dic['quarter'] = data.quarter
			dic['mathematics'] = data.mathematics
			dic['litrature'] = data.litrature
			dic['computer'] = data.computer
			output_list.append(dic)

		self.response.headers['Content-Type'] = 'application/json'
		self.response.out.write(json.dumps(output_list))

	def post(self):
		logging.debug("POST Recieved")
		post_data = student.PROPERTY_DICT.copy()
		error_flag = False
		for p in student.PROPERTY_DICT.keys():
			value = student.PROPERTY_DICT[p](self.request.get(p))
			logging.debug("Value of " + p + " : " + str(value))
			if value:
				if type(value) == student.PROPERTY_DICT[p]:
					post_data[p] = value
				else:
					REPLY_DICT[STATUS_KEY] = STATUS_ERROR
					REPLY_DICT[DESC_KEY] = "Unsuppoted Type " + str(type(value)) + " of " + p
					error_flag = True
					break
			else:
				REPLY_DICT[STATUS_KEY] = STATUS_ERROR
				REPLY_DICT[DESC_KEY] = "Property " + p + " not found"
				error_flag = True
				break

		try:
			post_data['dob'] = self.format_date(post_data['dob'])
		except:
			REPLY_DICT[STATUS_KEY] = STATUS_ERROR
			REPLY_DICT[DESC_KEY] = "DOB not in proper format. Required: 'yyyy-mm-dd' Not: " + str(post_data['dob'])
			error_flag = True
		

		if error_flag:
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(REPLY_DICT))
		elif not self.check_date(post_data['dob']):
			REPLY_DICT[STATUS_KEY] = STATUS_ERROR
			REPLY_DICT[DESC_KEY] = "DOB not in proper format. Required: 'yyyy-mm-dd' Not: " + str(post_data['dob'])
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(REPLY_DICT))
		elif not self.check_quarter(post_data['quarter']):
			REPLY_DICT[STATUS_KEY] = STATUS_ERROR
			REPLY_DICT[DESC_KEY] = "QUARTER not in proper format. Required: Q1-Q4"
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(REPLY_DICT))
		else:

			students = student.get_by_student_id(post_data['id'])

			if students:
				if isinstance(students, collections.Iterable):
					for s in students:
						if s.quarter == post_data['quarter']:
							error_flag = True
				else:
					if students.quarter == post_data['quarter']:
							error_flag = True

			if(error_flag):
				REPLY_DICT[STATUS_KEY] = STATUS_ERROR
				REPLY_DICT[DESC_KEY] = "QUARTER already exists"
				self.response.headers['Content-Type'] = 'application/json'
				self.response.out.write(json.dumps(REPLY_DICT))
			else:
				post_data['dob'] = datetime.datetime.strptime(post_data['dob'], '%d%m%Y').date()
				id = self.create_student(post_data)
				REPLY_DICT[STATUS_KEY] = STATUS_OK
				REPLY_DICT[DESC_KEY] = "Student ID: " + str(post_data['id'])
				self.response.headers['Content-Type'] = 'application/json'
				self.response.out.write(json.dumps(REPLY_DICT))