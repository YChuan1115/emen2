from test import *

vp = Database.datastorage.valid_properties
rvp = {}
for k,v in vp.items():
	for i in v[1]:
		rvp[i]=k
	for i in v[2]:
		rvp[i]=k
		
rvp[None]="none"
rvp[""]="empty"
#print rvp

import demjson
jsvp = {}
for k,v in vp.items():
	jsvp[k]=[v[0],v[1].keys()]
print demjson.encode(jsvp)



#import sys
#sys.exit(0)

for i in db.getparamdefnames(ctxid):
 	z=db.getparamdef(i)
 	if z.defaultunits != None and z.defaultunits != "":
		try:
			if rvp[z.defaultunits] != z.property:
				print "Need to fix: %s"%z.name
				print "\tdu: %s\n\tprop: %s -> %s"%(z.defaultunits, z.property, rvp[z.defaultunits])
				z.property=rvp[z.defaultunits]
				db.addparamdef(z,ctxid)

		except:
			print "wtf %s, %s"%(z.name, z.defaultunits)
			
			