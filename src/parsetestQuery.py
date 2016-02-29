import json,httplib,urllib
connection = httplib.HTTPSConnection('api.parse.com', 443)
params = urllib.urlencode({"where":json.dumps({
       "score": {
         "$gte": 1000,
         "$lte": 3000
       }
     })})
connection.connect()
connection.request('GET', '/1/classes/GameScore?%s' % params, '', {
       "X-Parse-Application-Id": "1B4lAQPlSyf21OWEW4wsBxHGJtJOD5K2zQ4wquUH",
       "X-Parse-REST-API-Key": "GO8568E0Uw5j6kNidppxqyTJBXc4x6JSvE1rv3pj"
     })
result = json.loads(connection.getresponse().read())
print result


