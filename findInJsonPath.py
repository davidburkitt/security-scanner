import json, sys
from jsonpath_ng import jsonpath, parse

with open(sys.argv[1]) as json_file:
  json_data = json.load(json_file)

#jsonpath_expression = parse('last_run.summary.*.flagged_items')
jsonpath_expression = parse(sys.argv[2])
for match in jsonpath_expression.find(json_data):
  if isinstance(match.value,int):
    if match.value > 0:
      print(str(match.full_path)+":"+str(match.value))
  if isinstance(match.value,dict):
    print(json.dumps(match.value, indent=4, sort_keys=True))

