#coding: utf-8
import urllib,urllib2,cookielib,html5lib,time,string
from bs4 import BeautifulSoup

import smtplib
from email.mime.text import MIMEText

post_data = {
    'numberItems':'1',
    'officeId':'548',   #DMV officeID, e.g. 548 is the ID for Redwood City, CA
    'requestedTask':'DT',
    'firstName':'yourFirstName',
    'lastName':'yourLastName',
    'dlNumber':'yourPermitNumber',
    'birthMonth':'yourBirthMonth',
    'birthDay':'yourBirthday',
    'birthYear':'yourBirthYear',
    'telArea':'PhoneArea',
    'telPrefix':'PhonePrefix',
    'telSuffix':'PhoneSuffix',
    'resetCheckFields':'true'
}

flag = False

while True:
    myCookie = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
    opener = urllib2.build_opener(myCookie)
    try:
        req = urllib2.Request('https://www.dmv.ca.gov/wasapp/foa/findDriveTest.do',urllib.urlencode(post_data))
        html_src = opener.open(req).read()
    except urllib2.URLError,e:
        print 'try again'
        continue
    except urllib2.HTTPError,e:
        print 'try again'
        continue
    parser = BeautifulSoup(html_src,"html5lib")

    article = parser.findAll('p','alert')

    #result is used for testing
    #output is used for emailing
    #result = []
    output = ''
    for sub in article:
        state = []
        for tag in sub.contents:
            factor = tag.string
            state.append(factor)
    #    result.append(' '.join(state))
        output = output + ' '.join(state)
    
    #for index in range(len(result)):
    #    print result[index]

    print output
    str_split = output.split(',')
    target = str_split[len(str_split)-2].split(' ')
    try:
        Mon = target[1]
        Day = target[2]
    except IndexError:
        continue
    #e.g. set the day to be between 08/25 to 09/19
    if (Mon == 'September' and string.atoi(Day)<19)or(Mon == 'August' and string.atoi(Day)>25):
        flag = True
        break
    
    time.sleep(30)

if flag:    
    username = 'username' # username
    password = 'userpassword' # password

    sender = 'userEmail' # sender email
    receiver = 'userEmail' # receiver email
    subject = 'python email test'
    mail_content = output
    msg = MIMEText(mail_content,'plain','utf-8')
    msg['Subject'] = subject

    mail_server = 'smtp.gmail.com'
    mail_server_port = 587
    server = smtplib.SMTP(mail_server, mail_server_port)
    # server.set_debuglevel(1) # debug mode
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()

