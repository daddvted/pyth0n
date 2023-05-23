import smtplib, ssl

port = 587  # For starttls
smtp_server = "mail.shit.com"
sender_email = "luna_help@shit.com"
receiver_email = "67784480@qq.com"
password = "zdsys8301"
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP(smtp_server, port) as server:
    server.ehlo()  # Can be omitted
    server.starttls(context=context)
    server.ehlo()  # Can be omitted
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)