import json,httplib

APPLICATION_ID = "1B4lAQPlSyf21OWEW4wsBxHGJtJOD5K2zQ4wquUH"
REST_API_KEY = "GO8568E0Uw5j6kNidppxqyTJBXc4x6JSvE1rv3pj"
MASTER_KEY = "MRv0ZczdLEsccVxWYAdlaF1aIV3EM3iUl2sP7pKb"

connection = httplib.HTTPSConnection('api.parse.com', 443)
connection.connect()
connection.request('POST', '/1/schemas/ItemPrice', json.dumps({
     "className":"ItemPrice","fields":{"desc":{"type":"String"}, "ign":{"type":"String"}, "price":{"type":"Number"}
                                       , "currencyTo":{"type":"String"}, "isOnline":{"type":"Boolean"}, "itemInfo":{"type":"String"} }
     }), {
       "X-Parse-Application-Id": APPLICATION_ID,
       "X-Parse-Master-Key": MASTER_KEY,
       "Content-Type": "application/json"
     })
result = json.loads(connection.getresponse().read())

print result
