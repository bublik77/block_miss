#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from twilio.rest import Client

def call(name='cryptolions'):
    try:
        load_dotenv()
    except:
        print("can't get value")
    
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    call = client.calls.create(
                        twiml=f'<Response><Say>Ahoy, {name} World!</Say></Response>',
                        to=os.environ['NUM_TO'],
                        from_=os.environ['NUM_FROM']
                    )
    print(account_sid, auth_token)
    print(call.sid)


if __name__== "__main__":
    call()

