#!/usr/bin/env python

'''

This script should be placed at A2 hosting under ~/dev/ and be run with crontab every 12 hours
It writes to a txt file located at jakobsen.ca/data/cida.txt

Monitor Data sources for Open Aid Data Explorer: Canadian aid projects around the world - 

Files listed are used at: 

http://cidpnsi.ca/blog/portfolio/open-aid-data-explorer-canadian-aid-projects-around-the-world/

'''

from time import gmtime, strftime
import httplib
cida_csv_url="www.acdi-cida.gc.ca"
conn = httplib.HTTPConnection(cida_csv_url)
conn.request("HEAD", "/cidaweb/cpo.nsf/vLUOpenDataFile/PBOpenData/$file/Project%20Browser%20English.csv")
res = conn.getresponse()
print res.status, res.reason

headers = res.getheaders()
last_mod = dict(headers)['last-modified']
print "Last modified in HTTP headers at CIDA"
print last_mod


now =  strftime("%Y-%m-%d %H:%M:%S", gmtime())
print "Last time headers were checked"
print now
f = open("/home/jakobsen/public_html/data/cida.txt","w") #opens file with name of "test.txt"
f.write("'last-checked:'"+now)
f.write("\n")
f.write("'last-modified:'"+last_mod)
f.close()