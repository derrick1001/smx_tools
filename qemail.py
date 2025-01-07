import smtplib
from email.message import EmailMessage
from sys import argv

subj = input("Subject: ")
cc = list(input("Cc: "))


def email(subj: str, cont: str) -> None:
    msg = EmailMessage()
    msg.set_content(cont)
    msg["Subject"] = subj
    msg["From"] = "nms@mycvecfiber.com"
    msg["To"] = "dishman@cvecfiber.com"
    msg["Cc"] = cc
    s = smtplib.SMTP("10.20.7.31")
    s.send_message(msg)
    s.quit()


with open("cont.txt", "r") as cont:
    email(subj, cont)
