import StudentHandler
import TeacherHandler
import webapp2

app = webapp2.WSGIApplication([
	('/', StudentHandler.Default),
	('/student', StudentHandler.SubmitStudent), 
	('/student/(\d+)', StudentHandler.SingleStudent),
	('/statistics/studentperquarter/(\d+)', StudentHandler.QuaterAnalysis),
	('/statistics/quarter/(\d+)', StudentHandler.SubjectAnalysis),
	('/statistics/quarter', StudentHandler.SubjectQuaterAnalysis),

	('/teacher/statistics/quarter', TeacherHandler.DisplaySubjectQuaterAnalysis),
	('/teacher/statistics/quarter/(\d+)', TeacherHandler.DisplaySubjectAnalysis),
	('/teacher/statistics/studentperquarter/(\d+)', TeacherHandler.DisplayQuaterAnalysis),

	('/teacher', TeacherHandler.MainForm),
], debug=True)