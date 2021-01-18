"""

 Created by Razvan at 1/1/2021


"""

import smtplib
import ssl
import datetime
from email.mime.text import MIMEText


def get_contacts(filename):
    """Function to get the separate the username and the email from the email_list file"""

    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
            print("emails: ", emails)
            print("names: ", names)
    return names, emails


def send_email(followers, unfollowers, receiver, receiver_name, password, sender):
    """ Function to simplify the sending of emails. Works for Gmail only. Other SMTP servers can be configured"""

    smtp_server = 'smtp.gmail.com'
    port = 465
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d")

    subject = "Here's your summary for {}".format(now)
    text_subtype = 'plain'
    content = """\
    Hey {}!

    Here's your Instagram summary for today:

    New followers: {}

    Unfollowers: {}


    This message was generated&sent from ShitstaBot!
    Buh'bye
    """.format(receiver_name, followers, unfollowers)
    print("Sent email: \n", content)
    msg = MIMEText(content, text_subtype)

    context = ssl.create_default_context()
    msg['Subject'] = subject
    msg['From'] = sender

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())

    return None
