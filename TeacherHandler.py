import urllib2
import json
# import numpy as np
import cStringIO
# import webapp2
# import jinja2

# import os
# os.environ["MATPLOTLIBDATA"] = os.getcwdu()
# os.environ["MPLCONFIGDIR"] = os.getcwdu()
# import subprocess
# def no_popen(*args, **kwargs): raise OSError("forbjudet")
# subprocess.Popen = no_popen
# subprocess.PIPE = None
# subprocess.STDOUT = None
# try:
#	 import matplotlib.pyplot as plt
# except:
#	 print "trouble"

import logging
try:
	import webapp2
except:
	logging.exception("no webapp")
import pprint
import os
import StringIO
os.environ["MATPLOTLIBDATA"] = os.getcwdu()
os.environ["MPLCONFIGDIR"] = os.getcwdu()
import subprocess
def no_popen(*args, **kwargs): raise OSError("forbjudet")
subprocess.Popen = no_popen
subprocess.PIPE = None
subprocess.STDOUT = None
logging.warn("E: %s" % pprint.pformat(os.environ))
try:
	import numpy, matplotlib, matplotlib.pyplot as plt
except:
	logging.exception("trouble")
	print "trouble"

from google.appengine.ext.webapp import template

STATUS_KEY = 'status'
DESC_KEY = 'description'

STATUS_ERROR = 'error'
STATUS_OK = 'ok'

REPLY_DICT = {STATUS_KEY: "", DESC_KEY: ""}

path = os.path.join(os.path.dirname(__file__), 'templates/submitStudent.html')

def make_plot(data, labels, title):

	assert(len(data) == len(labels))

	fig, ax = plt.subplots()
	ind = numpy.arange(1, len(data)+1)

	# show the figure, but do not block
	# plt.show(block=False)
	
	# q1, q2, q3, q4 = plt.bar(ind, data)
	# q1.set_facecolor('r')
	# q2.set_facecolor('r')
	# q3.set_facecolor('r')
	# q4.set_facecolor('r')

	plt.bar(ind, data)
	ax.set_xticks(ind)
	ax.set_xticklabels(labels)
	# ax.set_ylabel('Percent usage')
	ax.set_title(title)

	sio = cStringIO.StringIO()
	plt.savefig(sio, format="png")
	# plt.show()

	return sio

# print make_plot([2,4,6,3], ['Q1','Q2','Q3', 'Q4'], 'quarters')

class MainForm(webapp2.RequestHandler):
    def get(self):
		self.response.out.write(template.render(path, {}))

class DisplayQuaterAnalysis(webapp2.RequestHandler):
	
	SUBJECT_LIST = ['mathematics', 'computer', 'litrature']

	def get(self, student_id):
		url = "http://" + str(self.request.host) + "/statistics/studentperquarter/" + str(student_id)
		print "URL: " + url
		response = urllib2.urlopen(url, timeout=100)
		data = json.load(response)

		if data['status'] == 'ok':
			desc = data['description']

			self.response.write("""<html><body>""")

			vals = []
			for q in desc.keys():
				vals.append(desc[q])
			Q1P = make_plot(vals, desc.keys(), "Quater Analysis for Student: " + student_id)

			img_b64 = Q1P.getvalue().encode("base64").strip()
			self.response.write("<img src='data:image/png;base64,%s'/><br>" % img_b64)
			
			self.response.write("""</body> </html>""")

		else:
			REPLY_DICT[STATUS_KEY] = STATUS_ERROR
			REPLY_DICT[DESC_KEY] = data['description']
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(REPLY_DICT))


class DisplaySubjectAnalysis(webapp2.RequestHandler):
	
	SUBJECT_LIST = ['mathematics', 'computer', 'litrature']

	def get(self, subject):
		url = "http://" + str(self.request.host) + "/statistics/quarter/" + str(subject)
		print "URL: " + url
		response = urllib2.urlopen(url, timeout=100)
		data = json.load(response)

		if data['status'] == 'ok':
			desc = data['description']

			self.response.write("""<html><body>""")

			vals = []
			for q in desc.keys():
				vals.append(desc[q])
			Q1P = make_plot(vals, desc.keys(), self.SUBJECT_LIST[int(subject)])

			img_b64 = Q1P.getvalue().encode("base64").strip()
			self.response.write("<img src='data:image/png;base64,%s'/><br>" % img_b64)
			
			self.response.write("""</body> </html>""")

		else:
			REPLY_DICT[STATUS_KEY] = STATUS_ERROR
			REPLY_DICT[DESC_KEY] = data['description']
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(REPLY_DICT))


class DisplaySubjectQuaterAnalysis(webapp2.RequestHandler):
	
	def get(self):
		url = "http://" + str(self.request.host) + "/statistics/quarter"
		print "URL: " + url
		response = urllib2.urlopen(url, timeout=100)
		data = json.load(response)

		if data['status'] == 'ok':
			desc = data['description']

			self.response.write("""<html><body>""")

			vals = []
			Q1 = desc['Q1']
			for q in Q1.keys():
				vals.append(Q1[q])
			Q1P = make_plot(vals, Q1.keys(), "Quater1")

			img_b64 = Q1P.getvalue().encode("base64").strip()
			self.response.write("<img src='data:image/png;base64,%s'/><br>" % img_b64)

			vals = []
			Q2 = desc['Q2']
			for q in Q2.keys():
				vals.append(Q2[q])
			Q2P = make_plot(vals, Q2.keys(), "Quater2")

			img_b64 = Q2P.getvalue().encode("base64").strip()
			self.response.write("<img src='data:image/png;base64,%s'/><br>" % img_b64)

			vals = []
			Q3 = desc['Q3']
			for q in Q3.keys():
				vals.append(Q3[q])
			Q3P = make_plot(vals, Q3.keys(), "Quater3")

			img_b64 = Q3P.getvalue().encode("base64").strip()
			self.response.write("<img src='data:image/png;base64,%s'/><br>" % img_b64)

			vals = []
			Q4 = desc['Q4']
			for q in Q4.keys():
				vals.append(Q4[q])
			Q4P = make_plot(vals, Q4.keys(), "Quater4")

			img_b64 = Q4P.getvalue().encode("base64").strip()
			self.response.write("<img src='data:image/png;base64,%s'/><br>" % img_b64)
			
			self.response.write("""</body> </html>""")



		else:
			REPLY_DICT[STATUS_KEY] = STATUS_ERROR
			REPLY_DICT[DESC_KEY] = data['description']
			self.response.headers['Content-Type'] = 'application/json'
			self.response.out.write(json.dumps(REPLY_DICT))