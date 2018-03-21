#!/usr/bin/python
# -*- coding: UTF-8 -*-
#author: elina.ma@blackboard.com
#This script has been tested via python 3.6
'''
 If you want to get all provisioned sites' instance id on AWS, 
 please run 'python3 captain.py all'.
 If you want to get provisioned sites' instance id which belong to 
test envirionment, please run 'python3 captain.py Testing'
and 'pythons captain.py test'.
 The sum of the two 'client-ids' files from script's output
is instanceid for all sites provisioned on test environment. 
'''
import base64
import requests

import sys

base_url='http://captain.bbpd.io/api/'
captain_username = base64.b64decode('yourusername').decode()
captain_password = base64.b64decode('yourpassword').decode()

def httpclient(api_url,  username, password):

	response = requests.get(api_url, auth=(username, password), timeout=10)
	if not response.ok:
		raise Exception('{}: {}'.format(response.status_code, response.text))
	return response

if len(sys.argv) >= 2:
	envinfo =  sys.argv[1]
else:
	envinfo = 'all'
print(envinfo+"&&&&&&&&&&&&&&&&")

api_url = base_url + 'learns.json?limit=5000'
response = httpclient(api_url, captain_username, captain_password)

#print (response.json()[0])

f = open('client-ids','w')
f.write("id-entityid,url,captainid,identifyingtag,environment,update_at\n")
try:
	for i in range(len(response.json())):
		#print (len(response.json()))
		site = response.json()[i]
		#if (site['environment'] == envinfo):
		if ((envinfo in site['environment']) or (envinfo == 'all')):
			#listSite = list(site.values())
			#print(site)
			sublist = [str(site['id']),site['url'], \
					site['captainid'],site['identifyingtag'], \
					site['environment']]
			strinfo = ','.join(sublist)	

			api_url = base_url +'learns/' + str(site['id']) \
						+'/logs.json'
			res = httpclient(api_url, captain_username, captain_password)

			if len(res.json()) > 0 :
				#print('*************'+ res.text)
				for j in range(len(res.json())):
					loginfo = res.json()[j]
					if (('rolling_restart' in loginfo['description']) or \
						('codeline_upgrade' in loginfo['description']) or \
						('update_learn_b2' in loginfo['description']) or \
						('provision_learn' in loginfo['description'])):
						strinfo += ',' + loginfo['updated_at']
						break
			f.write(strinfo + '\n')
finally:
	f.close()


