import smtplib
from email.message import EmailMessage
from datetime import date

from calix.path import cvec_alrms


def email(e9, alrm_name):
    with open(
        f"{cvec_alrms}/{alrm_name}/{e9}/{e9}_{date.today()}_{alrm_name}.txt", "r"
    ) as f:
        msg = EmailMessage()
        msg.set_content(f.read())
    msg["Subject"] = input("Subject: ")
    msg["From"] = input("From: ")
    msg["To"] = input("To: ")
    msg["Cc"] = list(input("Cc: ").split())
    s = smtplib.SMTP("10.20.7.31")
    s.send_message(msg)
    s.quit()
