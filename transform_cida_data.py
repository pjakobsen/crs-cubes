# This Python file uses the following encoding: utf-8
import csv
import sys
import locale
import sqlite3
import sqlalchemy
from pprint import pprint
from countryinfo import countries



def continent(country):
    if country in  ["South Sudan","Saint Helena","Western Sahara","Burkina-Faso","Congo","Sao Tome and Principe","Turks and Caicos Islands","Gambia",u"Côte d'Ivoire","Africa multiple countries"]:
        return "Africa"
    elif country in ["Democratic People's Republic of Korea","Timor-Leste","Burma (Myanmar)","China","Asia multiple countries","Micronesia","Cook Islands","Niue"]:return "Asia"
    elif country in ["Anguilla","Montserrat","Cayman Islands","British Virgin Islands"]: return "North America"
    elif country in ["Europe multiple countries","Former Yugoslav Republic of Macedonia"]: return "Europe"
    elif country == "Americas multiple countries":
        return ""  
    else:
        return [c['continent'] for c in countries if c['name']==country][0]

print continent("Angola")    


def contribution(row):
    print row 
    sys.exit()

def read_file():
    
    with open(fil, 'rb') as f:
        reader = csv.reader(f)
        # Skip silly title that was appended to CSV file
        next(reader)
        header = next(reader)
        print header
        sys.exit()
        for i,row in enumerate(reader):
            print i
            contribution(row)



def dict_read(f):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    csv_file = csv.DictReader(open(f, 'rb'), delimiter=',', quotechar='"')
    #You can now parse through the data as a normal array.
    contributions=[]
    # skip the first line
    for i,line in enumerate(csv_file):
        
   
        country_line = line['Country']
        project_number=line['Project Number']
        dollars = line["Maximum CIDA Contribution"]
        # cida_focus = line["CIDA Sector of Focus"]
        # dac_focus = line["DAC Sector"]
        # print dac_focus
        #dollar_decimal = float(dollars[1:].strip())
        try:
            amount = float(locale.atof(dollars.lstrip("$ ")))
        except ValueError:
            print i,dollars
            pass
       
        if "100%" in country_line:
            #print(country_line.split(": ")[0], amount)
            contributions.append((country_line.split(": ")[0],project_number, amount))
        else: 
            participating_countries = country_line.split("%,")
            percentages =  [(p.rstrip("%").split(": ")[0],project_number,(float(p.rstrip("%").split(": ")[1])/100)*amount) for p in participating_countries]
            
            
            contributions += percentages
     
    return contributions 


def create_db():
    # Create the table
    engine = sqlalchemy.create_engine('sqlite:///cida_norm.db')
    metadata = sqlalchemy.MetaData(bind = engine)
    project_table = sqlalchemy.Table("projects", metadata)

    if project_table.exists():
        project_table.drop(checkfirst=False)
         
    create_id=True
    if create_id:
        col = sqlalchemy.schema.Column('id', sqlalchemy.Integer, primary_key=True)
        project_table.append_column(col)
    col = sqlalchemy.schema.Column("country", sqlalchemy.Text)
    project_table.append_column(col)
    col = sqlalchemy.schema.Column("continent", sqlalchemy.Text)
    project_table.append_column(col)
    col = sqlalchemy.schema.Column("project_number", sqlalchemy.Text)
    project_table.append_column(col)
    col = sqlalchemy.schema.Column("contribution", sqlalchemy.Integer)
    project_table.append_column(col)
    project_table.create()
    return project_table
    
if __name__ == "__main__":
    
    table = create_db()
    print table
  
    project_file='data/Project Browser English.csv'
    amounts = dict_read(project_file)
    # with these amounts in a database, we can now set up a normalized database that can be cubed
    for i,a in enumerate(amounts):
        pass
        # print i, "-------"
        # print a[0],int(round(a[1]))
        # Text including country names is saved as 8-bit ascii, so it must be converted
        '''
        >>> print "C\xf4te d'Ivoire"
        C?te d'Ivoire
        >>> print u"C\xf4te d'Ivoire"
        C..te d'Ivoire
        '''
        print (a[0])
        print "--------"
        country=(a[0]).decode("UTF-8")
        if ", " in country: 
            split_country = country.split(", ")
            country = split_country[1] + " of " + split_country[0]
            
        print country
        data = {"country":country,
         "continent":continent(country),
         "project_number":a[1], 
         "contribution":int(round(a[2]))}
        print data
        i = table.insert()
        try:
            i.execute(data)
        except:
            raise
    
    
    
