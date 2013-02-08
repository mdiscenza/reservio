from reservio import get_db, init_db
from twilio.rest import TwilioRestClient
from config import account_sid, auth_token, secret_key, username, password 

client = TwilioRestClient(account_sid, auth_token)

db = get_db()
# recipiant_number = db.execute("select cellnumber from entries where id= %d" %reservation_id)
# recipiant_name = db.execute("select name from entries where id= %d" %reservation_id)
# message_body = "Hey %s, your table is ready! Please see the host right away!" %str(recipiant_name)
# message = client.sms.messages.create(to=recipiant_number, from_="+18602544361",body=message_body)