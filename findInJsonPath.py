import json, sys
from jsonpath_ng import parse

with open(sys.argv[1]) as json_file:
  json_data = json.load(json_file)

jsonpath_expression = parse(sys.argv[2])

skip = False
for match in jsonpath_expression.find(json_data):
  # Work around - unable to filter 'findings' e.g. services.*.findings.*[?(@.flagged_items > 0)].items,description
  # Because filter mechanism only applies to list object and findings are dict
  if isinstance(match.value,int):
    if match.value == 0:
      skip = True
      continue
    else:
      skip = False
      continue
  elif not skip:
    print(json.dumps(match.value, indent=4, sort_keys=True))