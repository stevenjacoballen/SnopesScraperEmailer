# This automated script scrapes the top 5 stories from Snopes.com and send them to an
# email address, daily. Automation via Windows Task Scheduler.
# ------
# Project inspiration: https://www.youtube.com/watch?v=Ikf6Xdox0Go.


# This will only work until May, 2022... Gmail is changing security Features.
import requests  # http requests
from bs4 import BeautifulSoup  # web scrapping
import smtplib  # email
# email body
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# sys date/time
import datetime
now = datetime.datetime.now()

# email body placeholder
content = ''


# extraction
def extract_news(url):
    print('Extracting Snopes stories')
    cnt = ''
    cnt += ('<b>Top 5 Snopes Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')

    for i, tag in enumerate(soup.find_all(attrs={'class': 'stretched-link', 'href': True})):
        if i < 5:
            cnt += (str(i+1)+' :: ' + '<a href="'+tag['href']+'">' + tag.text + '</a>' + "\n" + '<br>')
    return cnt

# function call
cnt = extract_news('https://www.snopes.com/')
content += cnt
content += '<br>--------<br>'
content += '<br><br>End of Message'

# send email
print('Drafting Email...')
SERVER = 'smtp.gmail.com'
PORT = 587
FROM = '*********@*****.***'
TO = '**********@*****.***'  # can be a list
PASS = '*****'

msg = MIMEMultipart()

msg['Subject'] = 'Top 5 Latest Fact-Checks from Snopes [Automated]' + ' ' + str(now.day) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print('Initializing Server...')

server = smtplib.SMTP(SERVER, PORT)
server.set_debuglevel(1)  # enable debug (see errors)
server.ehlo()
server.starttls()
server.login(FROM, PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()
