from twilio.rest import Client
import os

account = os.getenv('ACCOUNT')
token = os.getenv('TOKEN')
client = Client(account, token)


def send_sms(to, sms_body, sender=os.getenv('PHONE_NO')):

    return client.messages.create(to=to, from_=sender,
                                  body=sms_body)
