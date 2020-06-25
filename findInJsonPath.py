import json, sys
from jsonpath_ng import parse

flags = {"-file":[1,1],"-path":[1,1],"-marker":[1,0]}
props = {}

def help(errorMessage):
  """ Exit with help."""
  usage = "\n### Usage: -file <json-file> -path <json-path> -marker <marker-for-match>"
  sys.exit(errorMessage + usage)

def parseArgs():
  """ Parse input arguments. """
  global props, flags
  for flag in flags.keys():
    if flag in sys.argv:         
        if flags[flag][0]:
          if sys.argv.index(flag)+1 == len(sys.argv) or sys.argv[sys.argv.index(flag)+1] in flags.keys():
              help("### " + flag + " requires a value.")
          else:            
              props[flag] = sys.argv[sys.argv.index(flag)+1]
        else:
          props[flag] = 1
    else:
        if flags[flag][1]:
          help("### " + flag + " is a required flag.")

def find(json_data, jsonpath_expression, marker=None):
  """ apply json path expression to file content """
  result = []
  skip = False
  for match in jsonpath_expression.find(json_data):
    if "marker" in locals() and isinstance(marker,int):
      # Work around - unable to filter 'findings' e.g. services.*.findings.*[?(@.flagged_items > 0)].items,description
      # Because filter mechanism only applies to list object and findings are dict
      if isinstance(match.value,int):
        if match.value < marker:
          skip = True
          continue
        else:
          skip = False
          continue
      elif not skip:
        #print(json.dumps(match.value, indent=4, sort_keys=True))
        result.append(match.value)
    else:
      result.append(match.value)  
  return result

def main():
  parseArgs()
  with open(props["-file"]) as json_file:
    json_data = json.load(json_file)
  jsonpath_expression = parse(props["-path"])
  if "-marker" in props.keys():
    result = find(json_data, jsonpath_expression, int(props["-marker"]))
  else:
    result = find(json_data, jsonpath_expression, None)  
  print(json.dumps(result, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()