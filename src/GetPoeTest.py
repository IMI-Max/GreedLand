# -*- coding: utf-8 -*-
from lxml.html import parse, submit_form
import StringIO
import sys
import json,httplib,urllib

def doParse(desc, url):
    desc = desc.decode("utf-8")
    page = parse(url).getroot()

    strIgn = "//@data-ign"
    dIgn = page.xpath(strIgn)
    print len(dIgn)

    strBout = "//@data-buyout"
    dBout = page.xpath(strBout)
    print len(dBout)


    for i in range(0, len(dBout)):
        strDn="//tbody[@id='item-container-" + str(i) + "']//@data-name"
        strDv="//tbody[@id='item-container-" + str(i) + "']//@data-value"

        dian = [itemAttrName for itemAttrName in page.xpath(strDn) ]
        diav = [itemAttrValue for itemAttrValue in page.xpath(strDv) ]
        print len(dian)
        print len(diav)


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
    
    #'''s
    
    #print result
    #print len(result)
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
def quecyParse

url = "http://poe.trade/search/adukotonohotas"

currencyTo = "chaos"
print "Build Currency Dict(Map)"
resultJsonFromDb = queryCurrencyRatioDb(currencyTo)
dictFromCurrencyRatioDb = getCurrencyRatioFromDb(resultJsonFromDb)
print "Currency Dict(Map)"
print dictFromCurrencyRatioDb
print

desc = "CI甲 5ex"
print "Build ItemPrice Dict(Map)"
resultJsonFromDb = queryItemPriceDb(desc)
dictFromItemPriceDb = getDictFromDb(resultJsonFromDb)
print "ItemPrice Dict(Map)"
print dictFromItemPriceDb
print

#doParse(desc, url)
