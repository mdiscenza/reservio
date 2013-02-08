from twilio.rest import TwilioRestClient
from CONFIG import account_sid, auth_token

def sendmessage():
	client = TwilioRestClient(account_sid, auth_token)

	message = client.sms.messages.create(to="+18609162984", from_="+18602544361",body="You're Twilio FINALLY WORKS")
	print message.sid

if __name__ == '__main__':
	sendmessage()