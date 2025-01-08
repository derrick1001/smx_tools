import smtplib
from email.message import EmailMessage

subj = input("Subject: ")
fhand = open("cont.txt", "r")
cont = fhand.read()


def email(subj: str, cont: str) -> None:
    cc = list(input("Cc: "))
    msg = EmailMessage()
    msg.set_content(cont)
    msg["Subject"] = subj
    msg["From"] = "nms@mycvecfiber.com"
    msg["To"] = "dishman@cvecfiber.com"
    msg["Cc"] = cc
    s = smtplib.SMTP("10.20.7.31")
    s.send_message(msg)
    s.quit()


if __name__ == "__main__":
    email(subj, cont)
    fhand.close()
