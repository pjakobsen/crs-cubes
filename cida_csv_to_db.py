import urllib2
import sys
import sqlite3
import sqlalchemy
import messytables

cida_csv_url="http://www.acdi-cida.gc.ca/cidaweb/cpo.nsf/vLUOpenDataFile/PBOpenData/$file/Project%20Browser%20English.csv"

'''
response = urllib2.urlopen(local_file)
csv_file = response.read()
'''
csv_file ="data/Project Browser English.csv"
fh = open(csv_file, 'rb')


table_set = messytables.CSVTableSet(fh,delimiter=",")

# A table set is a collection of tables:

row_set = table_set.tables[0]


# guess header names and the offset of the header:
offset, headers = messytables.headers_guess(row_set.sample)


row_set.register_processor(messytables.headers_processor(headers))

# add one to begin with content, not the header:
row_set.register_processor(messytables.offset_processor(offset + 2))

# guess column types:
types = messytables.type_guess(row_set.sample, strict=True)

print types

#SQLite does not support date objects, so Text is used instead. Convert in/out in python
type_map= {messytables.types.StringType:sqlalchemy.Text,
           messytables.types.IntegerType:sqlalchemy.Integer,
           messytables.types.DecimalType:sqlalchemy.Numeric,
           messytables.types.DateType:sqlalchemy.Text, 
           }
           

# combine names and types:
csv_columns = zip(headers, types)

# Create the table
engine = sqlalchemy.create_engine('sqlite:///cida.db')
metadata = sqlalchemy.MetaData(bind = engine)
projects_table = sqlalchemy.Table("projects", metadata)
if projects_table.exists():
   projects_table.drop(checkfirst=False)

create_id=True
if create_id:
    col = sqlalchemy.schema.Column('id', sqlalchemy.Integer, primary_key=True)
    projects_table.append_column(col)

for c in csv_columns:
   col = sqlalchemy.schema.Column(c[0], type_map[type(c[1])])
   projects_table.append_column(col)
   
projects_table.create()

for row in row_set:
    data = {r.column: r.value for r  in row}

    i = projects_table.insert()
    try:
        i.execute(data)
    except:
        raise
        
    
