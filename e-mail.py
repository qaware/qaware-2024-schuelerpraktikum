import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

#HTML e-mail test'

# HTML message content
html = """\
<html>
  <head></head>
  <body># Email content
sender = 'from@fromdomain.com'
receivers = ['to@todomain.com']

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['From'] = 'From Person <from@fromdomain.com>'
msg['To'] = 'To Person <to@todomain.com>'
msg['Subject'] = 'SMTP 
    <p>This is an e-mail message to be sent in <b>HTML format</b></p>
    <p><b>This is HTML message.</b></p>
    <h1>This is headline.</h1>
  </body>
</html>
"""

# Attach HTML content to the email
part2 = MIMEText(html, 'html')
msg.attach(part2)

# Connect to SMTP server and send email
try:
    smtpObj = smtplib.SMTP()
    smtpObj.sendmail('nils.gerhard@qaware.de', 'nils.gerhard@qaware.de', msg.as_string())
    print("Successfully sent email")
except smtplib.SMTPException as e:
    print(f"Error: unable to send email. Error message: {str(e)}")