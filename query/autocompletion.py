from urllib import request
import requests
import json
import urllib

def autocomplete(text):
    data = urllib.parse.quote_plus(text, safe='')
    req = requests.get(f'https://www.google.com/complete/search?q={data}&client=gws-wiz&xssi=t&hl=en-US')

    result = []

    response = json.loads(req.text[4:])[0]
    length = len(response)

    for i in range(length):
        result.append(response[i][0].replace("<b>", '').replace("</b>", ''))

    return result
