#!/usr/bin/python

import json, cgi, random, cgitb, math

# uncomment the line below only if there are problems.  It will give you debugging info.  Put the comment back in
# after the problems are fixed in order to not horrifically break even the minimal security baked in here.
# cgitb.enable()

def checkPrev(sid):
    firstCheck = students[sid]['Firstname'] == fname
    lastCheck = students[sid]['Lastname'] == lname
    return (firstCheck, lastCheck)

def displayNew():
    if mode == "weighted":
        sid = weightScores()
    else:
        sid = random.randint(1, len(students) - 1)
    printStudent(sid)

def weightScores():
    weights = [float(s['Score']['Wrong'])+float(s['Score']['Skip'])-float(s['Score']['Right']) for s in students[1:]]
    if max(weights) <= 3:
        divisor = 1
    else:
        divisor = max(weights) / 3
    nonNegWeights = [max(x, 0) for x in weights]
    flatWeights= [math.ceil(x / divisor) for x in nonNegWeights]
    picklist = expandWeights(flatWeights)
    return picklist[random.randint(1, len(picklist) - 1)]


def expandWeights(weights):
    picklist = []
    for index, item in enumerate(weights):
        counter = item
        while counter >= 0:
            picklist.append(index + 1)
            counter -= 1
    return picklist




def displaySkipped(sid):
    print "The last student was %s %s <br>" % (students[sid]['Firstname'], students[sid]['Lastname'])
    print "and here is his/her photo: <br>"
    image = imgp + students[sid]['Photo']
    print "<img src=\"%s\"><br>" % image
    displayScore(sid)
    print "It's ok, here's another: <br>"
    students[sid]['Score']['Skip'] += 1.0
    displayNew()

def displayCorrect():
    print "Congratulations!  You got the last student right! <br>"
    displayScore(sid)
    print "Now here's another: <br>"
    students[sid]['Score']['Right'] += 1.0
    displayNew()

def displayFWrong(sid):
    print "You got the last name, %s, right.  Now let's get the first one, eh?<br>" % students[sid]['Lastname']
    displayScore(sid)
    students[sid]['Score']['Wrong'] += 0.5
    printStudent(sid)

def displayLWrong(sid):
    print "You got the first name, %s, right.  Now let's get the first one, eh?<br>" % students[sid]['Firstname']
    displayScore(sid)
    students[sid]['Score']['Wrong'] += 0.5
    printStudent(sid)

def displayWrong(sid):
    print "Wrong.  Try again. <br>"
    displayScore(sid)
    students[sid]['Score']['Wrong'] += 1.0
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
    print "Next student selection: <input type=\"radio\" name=\"mode\" value\"weighted\" checked>Weighted <input type=\"radio\" name=\"mode\" value\"uniform\">Uniform "
    print "<input type=\"submit\" value=\"Submit\"><br>"
    print "<a href=\"memnames.cgi?id=%s&skipped=yes&file=%s&pw=%s&mode=weighted\">Skip (weight next)</a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" % (sid, filename, password)
    print "<a href=\"memnames.cgi?id=%s&skipped=yes&file=%s&pw=%s&mode=uniform\">Skip (uniform next)</a> " % (sid, filename, password)
    print "</center></body></html>"

def displayScore(sid):
    print "<br>So far, your score for that student is: <br>"
    print "Right: %s, Wrong: %s, Skipped: %s<br>" % (str(students[sid]['Score']['Right']), str(students[sid]['Score']['Wrong']), str(students[sid]['Score']['Skip']))


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
mode = "weighted"

try:
    sid = int(form.getvalue('id'))
    fname = form.getvalue('fname')
    lname = form.getvalue('lname')
    mode = form.getvalue('mode')
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

with open(filename2, 'w') as outfile:
    json.dump(students, outfile)
