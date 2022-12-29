import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings

def send_mail(html=None,text='Email_body',subject='Hello word',from_email='',to_emails=[],token="",user_id=""):
    assert isinstance(to_emails,list)
    html=f'http://127.0.0.1:8000/forgetpasswordforuser/{user_id}/{token}'
    msg=MIMEMultipart('alternative')
    msg['From']=from_email
    msg['To']=", ".join(to_emails)
    msg['Subject']=subject
    txt_part=MIMEText(text,'plain')
    msg.attach(txt_part)

    html_part = MIMEText(f"<p>Here is your password reset token</p><h1>{html}</h1>", 'html')
    msg.attach(html_part)
    msg_str=msg.as_string()


    server=smtplib.SMTP(host='smtp.gmail.com',port=587)
    server.ehlo()
    server.starttls()
    server.login(settings.GMAILKEYS['username'],settings.GMAILKEYS['password'])
    server.sendmail(from_email,to_emails,msg_str)
    server.quit()



def full_mail(html=None,text='Email_body',subject='hello world',from_email='',to_emails=[]):
    assert isinstance(to_emails,list)
    msg=MIMEMultipart('alternative')
    msg['From']=from_email
    msg['To']=", ".join(to_emails)
    msg['Subject']=subject
    txt_part=MIMEText(text,'plain')
    msg.attach(txt_part)

    html_part = MIMEText(html, 'html')
    msg.attach(html_part)
    msg_str=msg.as_string()


    server=smtplib.SMTP(host='smtp.gmail.com',port=587)
    server.ehlo()
    server.starttls()
    server.login(settings.GMAILKEYS['username'],settings.GMAILKEYS['password'])
    server.sendmail(from_email,to_emails,msg_str)
    server.quit()