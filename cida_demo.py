'''

Cubes is all about facts.  A fact is a data cell in the cube, and cube is a collection of the facts
A face is something that is measurable, like a contract. 
A dimension is the context for the fact, location, time, type
Who signed the contract, how much was spent on the construction work, and where the transaction happen.

Also, cubes supports hierchies. So you can define levels for each dimension, eg. year month, day, or continent, continent, city

Levels and attributes
Hierarchy
Key Attributes
Label Attributes

"Multi-dimensional breadcrumbs"

'''

import cubes

model = cubes.load_model("cida_model.json")

ws = cubes.create_workspace("sql",model,url="sqlite:///cida.db")

cube = model.cube("projects")

browser = ws.browser(cube)

result = browser.aggregate(drilldown=["Country"])    

print result.summary
print "---------------------"
for c in result.cells:
    print c