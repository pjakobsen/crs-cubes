import sys
from pprint import pprint;
from sqlalchemy import *

from messytables import CSVTableSet, type_guess, \
  types_processor, headers_guess, headers_processor, \
  offset_processor, any_tableset


''' SET UP DB '''
#db = create_engine('sqlite:///foo.sqlite')

db=create_engine("postgres://localhost/crs")

db.echo = False  # Try changing this to True and see what happens

metadata = MetaData(db)

# get the CRS table which already exists
crs = Table('crs', metadata, autoload=True)



''' Read CVS '''
fh = open('data/canada2011.csv', 'rb')

# Load a file object:
table_set = CSVTableSet(fh,delimiter="|")


# A table set is a collection of tables:
row_set = table_set.tables[0]


# guess header names and the offset of the header:
offset, headers = headers_guess(row_set.sample)
row_set.register_processor(headers_processor(headers))

# add one to begin with content, not the header:
row_set.register_processor(offset_processor(offset + 1))

# guess column types:
types = type_guess(row_set.sample, strict=True)

# and tell the row set to apply these types to
# each row when traversing the iterator:
row_set.register_processor(types_processor(types))

def add_record(row):
    data = {r.column: r.value for r  in row}

    i = crs.insert()
    try:
        i.execute(data)
    except:
        raise
    
    



# now run some operation on the data:
for row in row_set:
  add_record(row)