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
	envinfo = 'tag'
print(envinfo+"&&&&&&&&&&&&&&&&")

base_url='http://captain.bbpd.io/api/'
captain_username = base64.b64decode('yourname').decode()
captain_password = base64.b64decode('yourpasswd').decode()
api_url = base_url + 'learns.json?limit=5000'

response = requests.get(api_url, auth=(captain_username, captain_password), timeout=10)
if not response.ok:
    raise Exception('{}: {}'.format(response.status_code, \
			response.text))
#print (response.json()[0])

f = open('client-ids','w')
f.write("url,captainid,identifyingtag,environment\n")
try:
	for i in range(len(response.json())):
		#print (len(response.json()))
		site = response.json()[i]
		#if (site['environment'] == envinfo):
		if envinfo in site['environment']:
			#listSite = list(site.values())
			#print(site)
			sublist = [str(site['id']),site['url'], \
					site['captainid'],site['identifyingtag'], \
					site['environment']]
			strinfo = ','.join(sublist)	

			log_url = base_url +'learns/' + str(site['id']) \
						+'/logs.json'
			res = requests.get(log_url, auth=(captain_username, \
					captain_password), timeout=10)
			if not res.ok:
				raise Exception('{}: {}'.format(res.status_code, \
								res.text))
			if len(res.json()) > 0 :
				#print('*************'+ res.text)
				for j in range(len(res.json())):
					loginfo = res.json()[j]
					if 'rolling_restart' in loginfo['description']:
						strinfo += ',' + loginfo['updated_at']
						break
					elif 'codeline_upgrade' in loginfo['description']:
						strinfo += ',' + loginfo['updated_at']
						break
					else:
						pass

			f.write(strinfo + '\n')
			
finally:
	f.close()

