#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from twilio.rest import Client

def envirement_data():
    try:
        load_dotenv()
    except:
        print("can't get value")

def call(number, name=' ', chain=' '):
    space = "  "
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    call = client.calls.create(
                    twiml=f'<Response><Say>{space}{space}producer {name} miss a round in {chain} chain! {space} producer, {name} miss a round in {chain} chain!</Say></Response>',
                    to= number,
                    from_=os.environ['NUM_FROM']
                    )
    print(account_sid, auth_token)
    print(call.sid)


if __name__== "__main__":
    envirement_data()
    for i in os.environ["NUM_TO"].split(" "):
        call(i)