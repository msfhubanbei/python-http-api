#!/usr/bin/python
# -*- coding: UTF-8 -*-
#author: elina.ma@blackboard.com
#This script need been run above python 2.18

import base64
import requests
import sys

if len(sys.argv) >= 2:
	envinfo =  sys.argv[1]
else:
	envinfo = 'Staging'
print(envinfo+"&&&&&&&&&&&&&&&&")

base_url='http://captain.bbpd.io/api/'
captain_username = base64.b64decode('yourname').decode()
captain_password = base64.b64decode('yourpasswd').decode()
api_url = base_url + 'learns.json?limit=5000'

response = requests.get(api_url, auth=(captain_username, captain_password), timeout=10)
if not response.ok:
    raise Exception('{}: {}'.format(response.status_code, response.text))
#print (response.json()[0])

f = open('client-ids','w')
f.write("url,captainid,identifyingtag,environment\n")
try:
	for i in range(len(response.json())):
		#print (len(response.json()))
		site = response.json()[i]
		if(site['environment'] == envinfo):
			#listSite = list(site.values())
			#print(site)
			sublist = [site['url'],site['captainid'],site['identifyingtag'],site['environment']]
			strinfo = ','.join(sublist)
			f.write(strinfo + '\n')
			
finally:
	f.close()

