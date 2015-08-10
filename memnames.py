#!/usr/bin/python

import json, cgi, random, cgitb

# uncomment the line below only if there are problems.  It will give you debugging info.  Put the comment back in
# after the problems are fixed in order to not horrifically break even the minimal security baked in here.
# cgitb.enable()

def checkPrev(id):
    firstCheck = students[id]['Firstname'] == fname
    lastCheck = students[id]['Lastname'] == lname
    return (firstCheck, lastCheck)

def displayNew():
    id = random.randint(1, len(students))
    printStudent(id)

def displaySkipped(id):
    print "The last student was %s %s <br>" % (students[id]['Firstname'], students[id]['Lastname'])
    print "and here is his/her photo: <br>"
    image = imgp + students[id]['Photo']
    print "<img src=\"%s\"><br>" % image
    print "It's ok, here's another: <br>"
    displayNew()

def displayCorrect():
    print "Congratulations!  You got the last student right! <br>"
    print "Now here's another: <br>"
    displayNew()

def displayFWrong(id):
    print "You got the last name, %s, right.  Now let's get the first one, eh?<br>" % students[id]['Lastname']
    printStudent(id)

def displayLWrong(id):
    print "You got the first name, %s, right.  Now let's get the first one, eh?<br>" % students[id]['Firstname']
    printStudent(id)

def displayWrong(id):
    print "Wrong.  Try again. <br>"
    printStudent(id)

def headprint():
    print "Content-Type: text/html\n\n"
    print "<html><head><title>Student Flashcards</title></head><body>"
    print "<center>"

def printStudent(id):
    print "<br>"
    image = imgp + students[id]['Photo']
    print "<img src=\"%s\"><br>" % image
    print "<form action=\"memnames.cgi\" method=\"get\">"
    print "First Name: <input type=\"text\" name=\"fname\"><br>"
    print "Last Name: <input type=\"text\" name=\"lname\"><br>"
    print "<input type=\"hidden\" name=\"id\" value=\"%s\">" % id
    print "<input type=\"hidden\" name=\"pw\" value=\"%s\">" % password
    print "<input type=\"hidden\" name=\"file\" value=\"%s\">" % filename
    print "<input type=\"submit\" value=\"Submit\"><br>"
    print "<a href=\"memnames.cgi?id=%s&skipped=yes&file=%s&pw=%s\">Skip</a>" % (id, filename, password)
    print "</center></body></html>"



form = cgi.FieldStorage()
filename = form.getvalue('file')
filename2 = filename + '.json'

with open(filename2) as student_file:
  students = json.load(student_file)
# now we have a list of students, where each student is a dict of fn, ln, picture, and namemem score

imgp = students[0]["Imagepath"]

class AuthenticationError(Exception):
    pass

try:
    password = form.getvalue('pw')
except:
    raise AuthenticationError('no password')

if not password == students[0]['Password']:
    raise AuthenticationError('wrong password')

id = None
fname = None
lname = None
skipped = None

try:
    id = int(form.getvalue('id'))
    fname = form.getvalue('fname')
    lname = form.getvalue('lname')
except KeyboardInterrupt:
    raise
except:
    pass

try:
    id = int(form.getvalue('id'))
    skipped = form.getvalue('skipped')
except KeyboardInterrupt:
    raise
except:
    pass


headprint()

if id == None:
    displayNew()
elif skipped == "yes":
    displaySkipped(id)
else:
    last = checkPrev(id)
    if last == (True, True):
        displayCorrect()
    elif last == (False, True):
        displayFWrong(id)
    elif last == (True, False):
        displayLWrong(id)
    else:
        displayWrong(id)
