import cubes

model = cubes.load_model("model.json")

ws = cubes.create_workspace("sql",model,url="sqlite:///data.sqlite")

cube = model.cube("oecd_crs")

browser = ws.browser(cube)

result = browser.aggregate()

print result.summary