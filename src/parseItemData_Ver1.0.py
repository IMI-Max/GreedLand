# -*- coding: utf-8 -*-
from lxml.html import parse, submit_form
import StringIO
import sys
import json,httplib,urllib

def queryParseWorkList():
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    params = urllib.urlencode({"where":json.dumps({
           "isWork": True
         })})
    connection.connect()
    #'''
    connection.request('GET', '/1/classes/ParseWorkList?%s' % params, '', {
           "X-Parse-Application-Id": "1B4lAQPlSyf21OWEW4wsBxHGJtJOD5K2zQ4wquUH",
           "X-Parse-REST-API-Key": "GO8568E0Uw5j6kNidppxqyTJBXc4x6JSvE1rv3pj"
         })
    result = json.loads(connection.getresponse().read())
    
    return result['results']

def queryCurrencyRatioDb(currencyTo):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    params = urllib.urlencode({"where":json.dumps({
           "currencyTo": currencyTo
         })})
    connection.connect()
    #'''
    connection.request('GET', '/1/classes/CurrencyRatio?%s' % params, '', {
           "X-Parse-Application-Id": "1B4lAQPlSyf21OWEW4wsBxHGJtJOD5K2zQ4wquUH",
           "X-Parse-REST-API-Key": "GO8568E0Uw5j6kNidppxqyTJBXc4x6JSvE1rv3pj"
         })
    result = json.loads(connection.getresponse().read())
    
    #'''
    
    #print result
    #print len(result)
    return result['results']

def queryItemPriceDb(desc):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    params = urllib.urlencode({"where":json.dumps({
           "desc": desc
         })})
    connection.connect()
    #'''
    connection.request('GET', '/1/classes/ItemPrice?%s' % params, '', {
           "X-Parse-Application-Id": "1B4lAQPlSyf21OWEW4wsBxHGJtJOD5K2zQ4wquUH",
           "X-Parse-REST-API-Key": "GO8568E0Uw5j6kNidppxqyTJBXc4x6JSvE1rv3pj"
         })
    result = json.loads(connection.getresponse().read())
    
    #'''
    
    #print result
    #print len(result)
    #print desc.decode("utf-8") == result['results'][0]['desc']
    return result['results']

def getCurrencyRatioFromDb(resultJsonFromDb):
    dictFromDb = {}
    for i in resultJsonFromDb:
        dictFromDb[i['currencySrc']] = i['ratio']
        
    return dictFromDb

def getDictFromDb(resultJsonFromDb):
    dictFromDb = {}
    for i in resultJsonFromDb:
        dictFromDb[(i['desc'],i['ign'],i['price'])] = i
        
    return dictFromDb

def doParseAndGetDict(desc, url, dictFromCurrencyRatioDb, currencyTo):
    desc = desc.encode("utf-8")
    page = parse(url).getroot()

    strIgn = "//@data-ign"
    dIgn = page.xpath(strIgn)
    #print len(dIgn)

    strBout = "//@data-buyout"
    dBout = page.xpath(strBout)
    #print len(dBout)


    dictFromPoeGood = {}
    for i in range(0, len(dBout)):
        itemObj = {}
        ign = dIgn[i]
        strItemInfo = ""
        strDn="//tbody[@id='item-container-" + str(i) + "']//@data-name"
        strDv="//tbody[@id='item-container-" + str(i) + "']//@data-value"

        dian = [itemAttrName for itemAttrName in page.xpath(strDn) ]
        diav = [itemAttrValue for itemAttrValue in page.xpath(strDv) ]
        #print len(dian)
        #print len(diav)
        #print dian
        #print diav

        for j in range(1, (len(diav)-1)):
            strAttr = dian[j+2] + "--->[" + diav[j] + "]\n"
            strItemInfo += strAttr

        #print strItemInfo
        
        itemObj['desc'] = desc
        itemObj['ign'] = ign
        priceAry = dBout[i].split()
        if dictFromCurrencyRatioDb.get(priceAry[1]):
            itemObj['price'] = float(priceAry[0]) * dictFromCurrencyRatioDb.get(priceAry[1])
        else:
            itemObj['price'] = float(priceAry[0])
        
        itemObj['currencyTo'] = currencyTo
        itemObj['isOnline'] = True
        itemObj['itemInfo'] = strItemInfo
        dictFromPoeGood[(desc, ign, itemObj['price'])] = itemObj

    return dictFromPoeGood
    
def writeToDb(dictFromItemPriceDb, dictFromPoeGoodItemPrice):
    #Loop DB
    for keyInDb in dictFromItemPriceDb.keys():
        #can find in parse means need to update Online
        if(dictFromPoeGoodItemPrice.get(keyInDb)):
            updateParse(dictFromItemPriceDb.get(keyInDb), True)
        #can't find in parse means need to update Offline
        else:
            updateParse(dictFromItemPriceDb.get(keyInDb), False)

    #Loop PoeGood
    for keyInPoeGood in dictFromPoeGoodItemPrice:
        #can't find in Db means need to insert
        if(dictFromItemPriceDb.get(keyInPoeGood) == None):
            insertParse(dictFromPoeGoodItemPrice.get(keyInPoeGood))

def updateParse(itemObj, isOnline):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('PUT', '/1/classes/ItemPrice/'+itemObj['objectId'], json.dumps({
       "isOnline": isOnline
     }), {
       "X-Parse-Application-Id": "1B4lAQPlSyf21OWEW4wsBxHGJtJOD5K2zQ4wquUH",
       "X-Parse-REST-API-Key": "GO8568E0Uw5j6kNidppxqyTJBXc4x6JSvE1rv3pj",
       "Content-Type": "application/json"
     })
    results = json.loads(connection.getresponse().read())
    print results

def insertParse(itemObj):
    connection = httplib.HTTPSConnection('api.parse.com', 443)
    connection.connect()
    connection.request('POST', '/1/classes/ItemPrice', json.dumps(itemObj), {
       "X-Parse-Application-Id": "1B4lAQPlSyf21OWEW4wsBxHGJtJOD5K2zQ4wquUH",
       "X-Parse-REST-API-Key": "GO8568E0Uw5j6kNidppxqyTJBXc4x6JSvE1rv3pj",
       "Content-Type": "application/json"
     })
    results = json.loads(connection.getresponse().read())
    print results

currencyTo = "chaos"
print "Build Currency Dict(Map)"
resultJsonFromDb = queryCurrencyRatioDb(currencyTo)
dictFromCurrencyRatioDb = getCurrencyRatioFromDb(resultJsonFromDb)
print "Currency Dict(Map)"
print dictFromCurrencyRatioDb

resultJsonFromDb = queryParseWorkList()

for task in resultJsonFromDb:
    url = task['url']
    desc = task['desc']
    print
    print "**Task, " + desc + ", " + url + "**"
    print
    print "Build ItemPrice Dict(Map)"
    resultJsonFromDb = queryItemPriceDb(desc)
    dictFromItemPriceDb = getDictFromDb(resultJsonFromDb)
    #print "ItemPrice Dict(Map)"
    #print dictFromItemPriceDb
    print

    print "Build ItemPrice From PoeGood Dict(Map)"
    dictFromPoeGoodItemPrice = doParseAndGetDict(desc, url, dictFromCurrencyRatioDb, currencyTo)
    #print "PoeGoodItemPrice Dict(Map)"
    #print dictFromPoeGoodItemPrice
    print

    print "Write to DB"
    writeToDb(dictFromItemPriceDb, dictFromPoeGoodItemPrice)
