import json, sys
from jsonpath_ng import parse
import operator as op

flags = {"-file":[1,1],"-path":[1,1],"-index":[1,0],"-operand":[1,0],"-operator":[1,0]}
props = {}

def help(errorMessage):
  """ Exit with help."""
  usage = "\n### Usage: -file <json-file> -path <json-path> -index <index-field-for-match> -operand <operand-for-match> -operator <operator-for-match>"
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

def findInJSON(json_data, jsonpath_expression, index=None, operand=None, operator=None):
  """ apply json path expression to file content """
  operators = {
    ">": op.gt,
    "<": op.lt,
    "=": op.eq,
    "!=": op.ne}

  result = []
  skip = False
  for match in jsonpath_expression.find(json_data):
    if "operand" in locals() and isinstance(operand,int):
      # Work around - unable to filter 'findings' e.g. services.*.findings.*[?(@.flagged_items > 0)].items,description
      # Because filter mechanism only applies to list object and findings are dict
      if str(match.full_path).find(index) > -1:
      #if isinstance(match.value,int):        
        if operators[operator](match.value,operand):
        #if match.value < operand:
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
  if "-operand" in props.keys():
    result = findInJSON(json_data, jsonpath_expression, props["-index"], int(props["-operand"]), props["-operator"])
  else:
    result = findInJSON(json_data, jsonpath_expression, None)  
  print(json.dumps(result, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()