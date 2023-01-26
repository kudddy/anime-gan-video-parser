import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate


def send_mail(send_from, send_to, subject, message, files,
              server="smtp.gmail.com", port=465, username='', password=''):
    """Compose and send email with provided info and attachments.

    Args:
        send_from (str): from name
        send_to (list[str]): to name(s)
        subject (str): message title
        message (str): message body
        files (list[bytes]): list of file paths to be attached to email
        server (str): mail server host name
        port (int): port number
        username (str): server auth username
        password (str): server auth password
    """
    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = ', '.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(message))

    for data in files:
        part = MIMEBase('application', "octet-stream")
        part.set_payload(data)
        part.add_header('Content-Disposition',
                        'attachment; filename={}'.format(Path("data.csv").name))
        msg.attach(part)

    server = smtplib.SMTP_SSL(server, port)
    server.ehlo()
    server.login(username, password)
    server.sendmail(send_from, send_to, msg.as_string())
    server.close()
