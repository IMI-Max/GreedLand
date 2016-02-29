import json,httplib
connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()
connection.request('PUT', '/1/classes/GameScore/zBOPHn6RfH', json.dumps({
       "player_name": "Sean Plott",
       "cheat_mode": False
     }), {
       "X-Parse-Application-Id": "1B4lAQPlSyf21OWEW4wsBxHGJtJOD5K2zQ4wquUH",
       "X-Parse-REST-API-Key": "GO8568E0Uw5j6kNidppxqyTJBXc4x6JSvE1rv3pj",
       "Content-Type": "application/json"
     })
results = json.loads(connection.getresponse().read())
print results
