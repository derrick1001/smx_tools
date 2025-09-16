import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

fname = "cx.csv"


def email(subj: str) -> None:
    msg = MIMEMultipart()
    msg.attach(MIMEText("This file contains the affected subscribers.", "plain"))
    with open(fname, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={fname}")
    msg.attach(part)
    text = msg.as_string()
    msg["Subject"] = subj
    msg["From"] = "nms@mycvecfiber.com"
    msg["To"] = ["dishman@cvecfiber.com"]
    s = smtplib.SMTP("10.20.17.31")
    s.sendmail(msg["From"], msg["To"], text)
    s.close()


if __name__ == "__main__":
    email("")
