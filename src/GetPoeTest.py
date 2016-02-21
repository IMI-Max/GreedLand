from lxml.html import parse, submit_form
import StringIO
import sys

page = parse('http://poe.trade/search/adukotonohotas').getroot()

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

    




    
