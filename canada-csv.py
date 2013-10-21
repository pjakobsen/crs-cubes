import csv
import math
import sys
import locale
import os
import fnmatch

'''
Take OECD CRS files and extract Canadian projects.  Pick only the fields required in order to cut down on file size. 

Do a bunch of cleanup work on fields, then combine into a master csv file for canada

with open('canada/2011-mini-2.csv', 'rb') as data:
    rows = csv.reader(data)
    next(rows) #Skip the headers.
    row = next(rows)
    while r 
    print row
    #floats = [[float(item) for number, item in enumerate(row) if item and (1 <= number <= 12)] for row in rows]
'''
'''
['agencyname', 'crsid', 'projectnumber', 'recipientname', 'regionname', 'category', 'finance_t', 'aid_t', 'usd_commitment', 'usd_disbursement', 'usd_amountuntied_defl', 'projecttitle', 'purposecode', 'purposename', 'sectorcode', 'sectorname']

'''

locale.setlocale( locale.LC_ALL, '' )

fl = "/Users/peder/dev/Cubes/data/oecd-crs/CRS 2000-01 data.txt"

''' FIx the null bytes See http://stackoverflow.com/questions/4166070/python-csv-error-line-contains-null-byte
fi = open(fl, 'rb')
data = fi.read()
fi.close()
fo = open("/Users/peder/dev/Cubes/data/oecd-crs/CRS2000-01-new.csv", 'wb')
fo.write(data.replace('\x00', ''))
fo.close()
'''


new = "/Users/peder/dev/Cubes/data/oecd-crs/canada.csv"
new_fl = open(new, 'wb')
writer = csv.writer(new_fl)
writer.writerow(["year","agencyname","recipientname","regionname",'usd_commitment','usd_disbursement','projecttitle','purposename'])
csv.field_size_limit(sys.maxsize)

fm = {'completiondate': 52, 
        'usd_amountuntied_defl': 31, 
        'usd_export_credit': 37, 
        'usd_amountpartialtied_defl': 32, 
        'agencyname': 4, 
        'interest2': 69, 
        'longdescription': 53, 
        'purposename': 44, 'climateAdaptation': 64, 'interest1': 68, 'channelreportedname': 49, 'trade': 56, 'purposecode': 43, 'PBA': 59, 'usd_commitment': 20, 'sectorname': 46, 'usd_outstanding': 74, 'projecttitle': 42, 'bi_multi': 16, 'assocfinance': 61, 'geography': 50, 'category': 17, 'donorcode': 1, 'usd_commitment_defl': 23, 'usd_disbursement': 21, 'usd_expert_extended': 36, 'agencycode': 3, 'climateMitigation': 63, 'desertification': 65, 'investmentproject': 60, '\xff\xfeYear': 0, 'usd_amounttied': 30, 'environment': 55, 'numberrepayment': 67, 'incomegroupcode': 12, 'usd_amounttied_defl': 33, 'usd_interest': 73, 'expectedstartdate': 51, 'usd_disbursement_defl': 24, 'sectorcode': 45, 'projectnumber': 6, 'usd_future_DS_principal': 77, 'regionname': 11, 'pdgg': 57, 'usd_amountpartialtied': 29, 'repaydate1': 70, 'incomegroupname': 13, 'usd_adjustment_defl': 27, 'crsid': 5, 'currencycode': 38, 'commitment_national': 39, 'donorname': 2, 'aid_t': 19, 'regioncode': 10, 'usd_received': 22, 'usd_received_defl': 25, 'channelname': 48, 'recipientcode': 8, 'usd_expert_commitment': 35, 'typerepayment': 66, 'grantelement': 72, 'usd_amountuntied': 28, 'disbursement_national': 40, 'flowname': 15, 'biodiversity': 62, 'FTC': 58, 'gender': 54, 'usd_arrears_interest': 76, 'usd_adjustment': 26, 'channelcode': 47, 'initialreport': 7, 'usd_IRTC': 34, 'usd_arrears_principal': 75, 'usd_future_DS_interest': 78, 'finance_t': 18, 'flowcode': 14, 'recipientname': 9, 'shortdescription': 41, 'repaydate2': 71}

def curr(n):
    if n:
        #return locale.currency(complex(n).real*1000000,2,grouping=True)
        return round(complex(n).real*1000000,2)

def cleanme(t):
    if t:
        return t.split(" / ")[0].strip().title()  

def load_canada(fl) :  
    print fl
    with open(fl, 'rb') as f:
        mycsv = csv.reader(f,delimiter="|")
        header = next(mycsv)
        # Fieldmap
       
        for i, row in enumerate(mycsv):
    
            donorcode = row[1]
            
            if donorcode == '301':

                writer.writerow([row[0],row[fm['agencyname']],
                        row[fm['recipientname']],
                        row[fm['regionname']],
                        curr(row[fm['usd_commitment']]),
                        curr(row[fm['usd_disbursement']]),
                        cleanme(row[fm['projecttitle']]),
                        row[fm['purposename']]])
                
        
        # project_name =  row[11]
        # print 
        # if row[8]:
        #     print curr(row[8])
        #     print curr(row[9])
        f.close()
        
#load_canada(fl)
basedir="/Users/peder/dev/Cubes/data/oecd-crs/"

for dirpath, dirs, files in os.walk(basedir):
    for filename in fnmatch.filter(files, '*-new.csv'):
        load_canada(os.path.join(dirpath, filename))
new_fl.close()