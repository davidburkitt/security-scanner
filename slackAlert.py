import requests, json, sys
flags = {"-uri":[1,1],"-header":[1,1],"-title":[1,1],"-text":[1,1],"-colour":[1,1]}
props = {}

def help(errorMessage):
  """ Exit with help."""
  usage = "\n### Usage: -uri <slack-webhook> -header <msg-header> -title <msg-title> -text <msg-text> -colour <sidebar-colour>"
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

def buildPayload(header, title, text, colour):
  """ Construct message payload for Slack post """
  payload = """
  {
      "blocks": [
          {
              "type": "section",
              "text": {
                  "type": "mrkdwn",
                  "text": "__HEADER__"
              }
          },
          {
              "type": "divider"
          }
      ],
      "attachments": [
          {
              "color": "__COLOUR__",
              "title": "__TITLE__",
              "text": "__TEXT__"
          }
      ]
  }
  """
  for sub in (("__HEADER__", header), ("__TITLE__", title), ("__TEXT__",text), ("__COLOUR__",colour)):
      payload = payload.replace(*sub)
  return payload

def main():
  parseArgs()
  payload = buildPayload(props["-header"], props["-title"], props["-text"], props["-colour"])
  headers = {"content-type": "application/json"}
  r = requests.post(props["-uri"], headers = headers, data = json.dumps(json.loads(payload)))
  print(r.text)

if __name__ == "__main__":
  main()
