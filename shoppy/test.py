import os
from twilio.rest import Client
from django.conf import settings


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = ('ACe6819c922225f393518734cfe07deebd')
auth_token = ('765ca030c76f610974fa611906791d37')
client = Client(account_sid, auth_token)

message = client.messages.create(
                              body='Hi there',
                              from_='+12705173381',
                              to='+916238142442'
                          )
print(message.sid)

# def send_whatsapp_message(to,body):
#     account_sid = ('ACe6819c922225f393518734cfe07deebd')
#     auth_token = ('765ca030c76f610974fa611906791d37')
#     client = Client(account_sid, auth_token)
#     message = client.messages.create(
#                                 body= f'Thank You For Ordering With Us\n\nhere is ur transaction ID: {payment.payment_id}\n\n if you have any problems please contact with us.....',
#                                 from_='+12705173381',
#                                 to='+916238142442'
#                             )
    
    
# print(message.sid)

# print(message.sid)