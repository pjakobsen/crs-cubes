import sys
import sqlite3
import sqlalchemy
import messytables

from messytables import CSVTableSet, type_guess, \
  types_processor, headers_guess, headers_processor, \
  offset_processor, any_tableset

#SQLite does not support date objects, so Text is used instead. Convert in/out in python
type_map= {messytables.types.StringType:sqlalchemy.Text,
           messytables.types.IntegerType:sqlalchemy.Integer,
           messytables.types.DecimalType:sqlalchemy.Numeric,
           messytables.types.DateType:sqlalchemy.Text, 
           }






fh = open('data.csv', 'rb')

# Load a file object:
table_set = CSVTableSet(fh,delimiter="|")


# If you aren't sure what kind of file it is, you can use
# any_tableset.
#table_set = any_tableset(fh)

# A table set is a collection of tables:
row_set = table_set.tables[0]


# A row set is an iterator over the table, but it can only
# be run once. To peek, a sample is provided:
#print row_set.sample.next()

# guess header names and the offset of the header:
offset, headers = headers_guess(row_set.sample)


row_set.register_processor(headers_processor(headers))

# add one to begin with content, not the header:
row_set.register_processor(offset_processor(offset + 1))

# guess column types:
types = type_guess(row_set.sample, strict=True)


# combine names and types:
csv_columns = zip(headers, types)

# Create the table
engine = sqlalchemy.create_engine('sqlite:///foo.sqlite')
metadata = sqlalchemy.MetaData(bind = engine)
crs_table = sqlalchemy.Table("crs", metadata)
if crs_table.exists():
    crs_table.drop(checkfirst=False)





for c in csv_columns:
    col = sqlalchemy.schema.Column(c[0], type_map[type(c[1])])
    crs_table.append_column(col)



print crs_table
crs_table.create()
