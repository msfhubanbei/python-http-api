#!/usr/bin/python
# -*- coding: UTF-8 -*-
#author: elina.ma@blackboard.com
```
This script need been run above python 2.18
```
import base64
import requests

base_url='http://captain.bbpd.io/api/'
captain_username = base64.b64decode('your username').decode()
captain_password = base64.b64decode('your password').decode()

api_url = base_url + 'learns.json?limit=5000'

response = requests.get(api_url, auth=(captain_username, captain_password), timeout=10)
if not response.ok:
    raise Exception('{}: {}'.format(response.status_code, response.text))
print (response.json()[0])

f = open('client-ids','w')
try:
	for i in range(len(response.json())):
		#print (len(response.json()))
		site = response.json()[i]
		if(site['environment'] == 'Testing'):
			#print (str(site['clientid']))
			strid = str(site['clientid']) + '\n'
			f.write(strid)
finally:
	f.close()

