import json,httplib
connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()
connection.request('POST', '/1/schemas/City', json.dumps({
       "className":"City1","fields":{"name":{"type":"String"} }
     }), {
       "X-Parse-Application-Id": "1B4lAQPlSyf21OWEW4wsBxHGJtJOD5K2zQ4wquUH",
       "X-Parse-Master-Key": "MRv0ZczdLEsccVxWYAdlaF1aIV3EM3iUl2sP7pKb",
       "Content-Type": "application/json"
     })
result = json.loads(connection.getresponse().read())
print result
