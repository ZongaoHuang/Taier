import requests, pprint
import json

# payload = json.dumps(payload)

response = requests.get('http://localhost/api/test')

pprint.pprint(response)