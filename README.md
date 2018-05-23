# Grading-System
Grading System

⦁	Introduction

This application is created for teachers to maintain a record of student database on the web. The teacher can add a student and his/her marks in three subjects per quarter. Once entered a record cannot be deleted or modified. The Teacher can get list of all students or a particular student based on their unique student id, entered during record entry. The teacher may also view the average score of all students or one student per quarter and per subject in graphical representation.

⦁	Project Breakdown

The project is divided into two parts: a client and a server. The client is dependent on server, however, the server can operate on its own.

⦁	Server

The server contains the application program interface (API) and the database. It is intractable using web URLs. The server is programmed in python using the Google App Engine (GAE). Which is a free service available to run on local machines and provides limited hosting capabilities. The database used for this server is GAE’s GQL database. The server always returns in JSON.

⦁	APIs

https://udasity-training.appspot.com/teacher

The following are a few paths to interact with the APIs along with their specified paths.

⦁	Default:”/”

This returns a list of parameters and their datatypes required for adding a new student.

⦁	Student Data: “/student”

A GET request on this interface returns a list of all the students with their credentials. A POST request will add a student, provided that the parameters are correct according to the default API. 

⦁	Single Student Data: “/student/ID_OF_STUDENT”

A GET request on this link will return the information of a particular student. The student id is assigned at the time of adding the student.

⦁	Student Quarterly Average: “/statistics/studentperquarter/ID_OF_STUDENT”

This provides an average score per quarter of the student id thus entered.

⦁	Subject Quarterly Average: “/statistics/quarter”

Returns an average per quarter of all students per subject.

⦁	Subject Quarterly Average: “/statistics/quarter/ID_OF_SUBJECT”

This returns the quarterly average of all students for a given subject. The subject ids can be obtained by entering “id” as the ID_OF_SUBJECT.

⦁	Database:
The database is GQL which runs on Google App Engine (GAE). We created the following fields for a student.

{
'id':int,
'name':str,
'dob':str,
'class_name':str,
'year':int,
'quarter':str,
'mathematics':int,
'computer':int,
'litrature':int
}

Thus each student row will have columns explained above. We added checks for duplications as well. The id is to be provided by teacher for that purpose.

⦁	Client

The client interface is a web interface which is self-explanatory once used. It can be accessed at the “/teacher” path. It uses html and JavaScript as front-end while Google App Engine with python as back-end.
A screen shot is provided below:
 
The web app utilizes the APIs described in the last section to draw graphs of the required quarterly and subject-wise data. We used a python library called Matplotlib for that purpose.

⦁	Code
The project has the following files, explained with their uses.

⦁	Main

This file contains the URL redirection paths. It essentially routs traffic to the right handlers.

⦁	Student Handler

This file contains the http request handlers which serves each request according to demand.
⦁	Student

This is the database file for the student tables.

⦁	Teacher Handler

This is essentially the client handler. It deals with the main HTTP page along with creation of graphs.

⦁	Submit Student

This is an html file which contains the front page. It can be found in the templates folder within the project.

⦁	Building the Project

In order to run the project on your local machine or deploy it on the web you’ll need Google App Engine. It provides a free account and software to run on your machine.

Please follow the tutorial below to install and activate GAE:
https://cloud.google.com/appengine/docs/standard/python/quickstart?authuser=0

Once GAE is installed run the following command in the project folder for local machine:

dev_appserver.py app.yaml

For deployment on the web:

gcloud app deploy
