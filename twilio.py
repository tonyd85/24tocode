from twilio.rest import Client 
 
account_sid = 'AC7c35d6d25a694ba957e5243c9c5be4f0' 
auth_token = '' 
client = Client(account_sid, auth_token) 
 
message = client.messages.create( 
                              from_='+19193240870',        
                              to='+19198892549' 
                          ) 
 
print(message.sid)