from twilio.rest import Client

account_sid = 'AC1e3aaab55f7140eade64339494308923'
auth_token = '52c7e8be5c0a17e91736b1ce9e2f9c44'
client = Client(account_sid, auth_token)

message = client.messages \
    .create(
        from_='whatsapp:+14155238886',
        to='whatsapp:+919810660617',
        body='<Generic pyramid scheme>'
    )

print(message.sid)