import smtplib


sender = 'zhangpeng@shit.com'
receivers = ['67784480@qq.com']

message = """
This is a test e-mail message.
"""

smtpobj = smtplib.SMTP('mail.shit.com',25)

smtpobj.login('luna_help@shit.com', 'zdsys8301')
smtpobj.sendmail(sender, receivers, message)
print("Successfully sent email")