This is a small python application, meant to run as a CGI script, to memorize names with photos via flashcard.  This is designed to solve a problem of my own: the desire to have pervasive, platform-independent, flashcard capacity for memorizing student names.  

There are millions of apps for such purposes, but this one is mine, and it's very simple.  Give it some student names and picture filenames in JSON format.  Stick the files in the same folder.  Then go to it from any web browser.  It'll display pictures at random and a prompt to enter first and last name, or skip.  If you get it wrong, it shows the picture again.  If you get it right, it'll go to the next one.  If you skip, it'll display the answer then go to the next one.  

Usage: make a JSON like the example.  Put a password in the beginning.  Stick it in a cgi-bin somewhere with the extension changed to cgi.  Go to that URL, appending ?file=YOURFILENAME&pw=YOURPASSWORD to the end.  (no .json on your filename).  Stick the images in a different, non-cgi, directory (otherwise apache sometimes barfs).  Go to town.

Free to all under the MIT license.  

Note: for security and student privacy purposes, all files should be located in password-protected directories if it's on a publicly accessible webserver.  It's your responsibility to adequately secure this stuff.  The password at the beginning of the JSON is an extra layer of security, but it's a really weak and dumb layer (it's stored in clear and passed via http GET for goodness's sakes, although it shouldn't be too hard to change those things), and should not be relied upon.

Why?  Because javascript is ugly, and CGI died too soon.  

New functionality: it will also keep your score, so that you can see the students with whom you're struggling the most.  And there are two modes: uniform pick gives you each student with equal probability, weighted pick gives you the students whose names you have the most trouble with more often.  The weighting function is a little gnarly, so it might blow up, just let me know if it does.  Also, I don't *think* it'll run into horrible basins of attraction that just display the same student over and over, most of the gnarliness of the weights function is an attempt to prevent that, but I haven't actually tested it over large iterations, so if it does, just use uniform.



The MIT License (MIT)

Copyright (c) 2015, Paul Gowder

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
