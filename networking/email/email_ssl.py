import smtplib, ssl

port = 465  # For SSL
smtp_server = "mail.shit.com"
sender_email = "luna_help@shit.com"  # Enter your address
receiver_email = "597935388@qq.com"  # Enter receiver address
password = "zdsys8301"
message = """\
Subject: Hi there

This message is sent from Python."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

