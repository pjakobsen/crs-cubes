# Data preparation for the hello_world example

from sqlalchemy import create_engine
from cubes.tutorial.sql import create_table_from_csv

# 1. Prepare SQL data in memory

FACT_TABLE = "oecd_crs"

print "preparing data..."

engine = create_engine('sqlite:///data.sqlite')

create_table_from_csv(engine,
                      "sample.csv",
                      table_name=FACT_TABLE,
                      fields=[
                            ("year", "string"),
                            ("donorcode", "string"),
                            ("donorname", "string"),
                            ("agencycode", "string"),
                            ("agencyname", "string"),
                            ("crsid", "string"),
                            ("projectnumber", "string"),
                            ("initialreport", "string"),
                            ("recipientname", "string")],
                      create_id=True
                  )

print "done. file data.sqlite created"