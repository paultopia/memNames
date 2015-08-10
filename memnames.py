#!/usr/bin/python

import json, cgi, random, cgitb

# uncomment the line below only if there are problems.  It will give you debugging info.  Put the comment back in
# after the problems are fixed in order to not horrifically break even the minimal security baked in here.
# cgitb.enable()

def checkPrev(sid):
    firstCheck = students[sid]['Firstname'] == fname
    lastCheck = students[sid]['Lastname'] == lname
    return (firstCheck, lastCheck)

def displayNew():
    sid = random.randint(1, len(students))
    printStudent(sid)

def displaySkipped(sid):
    print "The last student was %s %s <br>" % (students[sid]['Firstname'], students[sid]['Lastname'])
    print "and here is his/her photo: <br>"
    image = imgp + students[sid]['Photo']
    print "<img src=\"%s\"><br>" % image
    print "It's ok, here's another: <br>"
    displayNew()

def displayCorrect():
    print "Congratulations!  You got the last student right! <br>"
    print "Now here's another: <br>"
    displayNew()

def displayFWrong(sid):
    print "You got the last name, %s, right.  Now let's get the first one, eh?<br>" % students[sid]['Lastname']
    printStudent(sid)

def displayLWrong(sid):
    print "You got the first name, %s, right.  Now let's get the first one, eh?<br>" % students[sid]['Firstname']
    printStudent(sid)

def displayWrong(sid):
    print "Wrong.  Try again. <br>"
    printStudent(sid)

def headprint():
    print "Content-Type: text/html\n\n"
    print "<html><head><title>Student Flashcards</title></head><body>"
    print "<center>"

def printStudent(sid):
    print "<br>"
    image = imgp + students[sid]['Photo']
    print "<img src=\"%s\"><br>" % image
    print "<form action=\"memnames.cgi\" method=\"get\">"
    print "First Name: <input type=\"text\" name=\"fname\"><br>"
    print "Last Name: <input type=\"text\" name=\"lname\"><br>"
    print "<input type=\"hidden\" name=\"id\" value=\"%s\">" % sid
    print "<input type=\"hidden\" name=\"pw\" value=\"%s\">" % password
    print "<input type=\"hidden\" name=\"file\" value=\"%s\">" % filename
    print "<input type=\"submit\" value=\"Submit\"><br>"
    print "<a href=\"memnames.cgi?id=%s&skipped=yes&file=%s&pw=%s\">Skip</a>" % (sid, filename, password)
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

sid = None
fname = None
lname = None
skipped = None

try:
    sid = int(form.getvalue('id'))
    fname = form.getvalue('fname')
    lname = form.getvalue('lname')
except KeyboardInterrupt:
    raise
except:
    pass

try:
    sid = int(form.getvalue('id'))
    skipped = form.getvalue('skipped')
except KeyboardInterrupt:
    raise
except:
    pass


headprint()

if sid == None:
    displayNew()
elif skipped == "yes":
    displaySkipped(sid)
else:
    last = checkPrev(sid)
    if last == (True, True):
        displayCorrect()
    elif last == (False, True):
        displayFWrong(sid)
    elif last == (True, False):
        displayLWrong(sid)
    else:
        displayWrong(sid)
