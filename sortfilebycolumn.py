#!/usr/bin/python
# -*- coding: UTF-8 -*-
#author: elina.ma@blackboard.com

f = open('client-ids')
listinfo = f.readlines()
listinfo1 = listinfo[1:]
#sorted by column 6 in file 'client-ids'
newlist = sorted(listinfo1, key=lambda s: s[5], reverse=True)
f.close()

print('*********' + str(newlist))

print('$$$$$$' + str(len(newlist)))
fnew = open('sorted-client-ids','w')
for line in range(len(newlist)):
	
	fnew.writelines(str(newlist[line]))
#	fnew.write('\n')
fnew.close()



