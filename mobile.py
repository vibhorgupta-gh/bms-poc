from twilio.rest import Client
import random, pickle, threading, time


def send_whatsapp(message_body):
    account_sid = 'AC1e3aaab55f7140eade64339494308923'
    auth_token = '52c7e8be5c0a17e91736b1ce9e2f9c44'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            from_='whatsapp:+14155238886',
            to='whatsapp:+919560741339',
            body=message_body
        )
    print(message.sid)

    if message.sid is None:
        return 'failed'
    return 'success'


def send_SMS(contact_no, code):
    account_sid = 'AC2e99fc3447e5740829859bea69a67b7b'
    auth_token = 'd15e347f4d5e039a21fea110bf511b11'

    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
            from_='+12055641962',
            to='+919560741339',
            body=code
        )
    print(message.sid)


def generate_otp(contact_no):
    try:
        otp = ''
        for x in range(6):
            otp = otp + str(random.randint(1,9))

        store = dict()
        store[str(contact_no)] = otp
        with open('contact_otp.pkl', 'wb') as otp_store:
            pickle.dump(store, otp_store)

        delete_thread = threading.Thread(target=delete_otp, args=(contact_no,))
        delete_thread.daemon = True
        delete_thread.start()
        print(otp)
        send_SMS(contact_no, otp)
        return 'success'
    except Exception as e:
        return str(e)


def check_otp(contact_no, code):
    try:
        store = dict()
        with open('contact_otp.pkl', 'rb') as otp_store:
            store = pickle.load(otp_store)

        otp = store[str(contact_no)]
        if otp is 'invalid_otp' or otp != code:
            return 'invalid'
        print(otp)
        return 'valid'
    except Exception as e:
        return str(e)


def delete_otp(contact_no):
    time.sleep(60)
    store = dict()
    with open('contact_otp.pkl', 'rb') as otp_store:
        store = pickle.load(otp_store)

    store[str(contact_no)] = 'invalid_otp'
    with open('contact_otp.pkl', 'wb') as otp_store:
        pickle.dump(store, otp_store)