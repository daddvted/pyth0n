from dingtalkchatbot.chatbot import DingtalkChatbot, ActionCard, CardItem
import sys,os
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=0958ca593ce11911c3d0d739d71ef9f1f3aae768c6b9420ba823734f403b12af'
secret = 'SECea0b091973f97de2fc849b6d84f6a2cb5832cc602140f7d8544aece0fa76c24d'

if len(sys.argv) > 3:
    subject = sys.argv[2]
    message = sys.argv[3].split('\r\n')
    #print(message)
    msg = '\n'.join(message)
    dingding_msg = "{0}\n{1}".format(subject, msg)
else:
    dingding_msg = "\n".join(sys.argv[1:])

#print(dingding_msg)
xiaoding = DingtalkChatbot(webhook, secret=secret)
xiaoding.send_text(msg=dingding_msg, at_mobiles=False)