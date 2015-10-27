#!/usr/bin/env python
"""
Fate & Fortune SMS.

Usage:
  fate-sms.py <mobile_number> [--password=<pwd>]
  fate-sms.py -h | --help

  The only parameter is your phone number preceded by the international
  dialing code +31 for the Netherlands.

Options:
  -h --help              Show this screen.
  -p --password=<pw>     Provide password.
"""
from twilio.rest import TwilioRestClient
from docopt import docopt
import json
from SimpleAES import SimpleAES  # military-grade bollocks!
import getpass

secret = """U2FsdGVkX1/x279RLQGfXryW2TiS01Mhlf7A2B7QoHQ1HSZd0IlBKbUaC4D9Pd8p\nJuHOKlM03ofoMQLTtxi50zO6wnRFASFA6DZ2J0e8llVk1uIi7A5MVprM5qblXCI4\nhHbr47inbe73zesmc+/n2MYcNSTLahegtdS+hSu8wM4="""

def decrypt_secret(passphrase="Haven't got a clue"):
    try:
        aes = SimpleAES(passphrase)
        dekret = aes.decrypt(secret)
        return json.loads(dekret)
    except Exception as e:
        print "(!!!) Damn! That was not the right password! Quick! Let's not waste precious time! Try again."

def send_sms_to(mobile, sid, token):
    client = TwilioRestClient(sid, token)
    myTwilioNumber = '+31852080387'
    print "Sending now an sms to", mobile
    message = client.messages.create(body="I'd give up if I were you or you'll never see her again. Quit your quest or deal with the consequences!", from_=myTwilioNumber, to=mobile)

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Fate')
    #print(arguments)

    if ('--password' in arguments) and (arguments['--password']):
        pw = arguments['--password']
    else:
        pw = getpass.getpass(prompt='Enter the shared secret: ')

    cred = decrypt_secret(pw)
    #print cred

    if cred and ('<mobile_number>' in arguments):
        send_sms_to(arguments['<mobile_number>'], cred['accountSID'], cred['authToken'])
