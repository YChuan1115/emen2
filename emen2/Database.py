##############
# Database.py  Steve Ludtke  05/21/2004
##############

"""This module encapsulates an electronic notebook/oodb

Note that the database does have a security model, but it cannot be rigorously enforced at the python level.
That is, a programmer using this library will not be able to accidentally violate the security model, but
with sufficient intent and knowledge it is possible. To use the module securely it must be encapsulated
by another layer, say an xmlrpc server...
"""

from bsddb3 import db
from cPickle import dumps,loads
from sets import *
import md5

LOGSTRINGS = ["SECURITY", "CRITICAL","ERROR   ","WARNING ","INFO    ","DEBUG   "]

class SecurityError(Exception):
	"Exception for a security violation"

class FieldError(Exception):
	"Exception for problems with Field definitions"

class BTree:
	"""This class uses BerkeleyDB to create an object much like a persistent Python Dictionary,
	keys and data may be arbitrary pickleable types"""
	def __init__(self,name,file=None,dbenv=None,nelem=0):
		"""This is a persistent dictionary implemented as a BerkeleyDB BTree
		name is required, and will also be used as a filename if none is
		specified"""
		global globalenv
		if (not dbenv) : dbenv=globalenv
		self.bdb=db.DB(dbenv)
		if file==None : file=name+".bdb"
#		print "Open: ",file
#		if nelem : self.bdb.set_h_nelem(nelem)					# guess how many elements in a hash
		self.bdb.open(file,name,db.DB_BTREE,db.DB_CREATE)
#		self.bdb.open(file,name,db.DB_HASH,db.DB_CREATE)

	def rmvlist(self,key,item):
		"""The keyed value must be a list of objects. 'item' will be removed from this list"""
		a=self[key]
		a.remove(item)
		self[key]=a

	def addvlist(self,key,item):
		"""The keyed value must be a list, and is created if nonexistant. 'item' is added to the list. """
		if (self.has_key(key)):
			self[key]=(self[key]+[item])
		else: self[key]=[item]

	def __del__(self):
		self.close()

	def close(self):
		self.bdb.close()

	def __len__(self):
		return len(self.bdb)

	def __setitem__(self,key,val):
		if (val==None) :
			self.__delitem__(key)
		else : self.bdb.put(dumps(key),dumps(val))

	def __getitem__(self,key):
		return loads(self.bdb.get(dumps(key)))

	def __delitem__(self,key):
		self.bdb.delete(dumps(key))

	def __contains__(self,key):
		return self.bdb.has_key(key)

	def keys(self):
		return map(lambda x:loads(x),self.bdb.keys())

	def values(self):
		return map(lambda x:loads(x),self.bdb.values())

	def items(self):
		return map(lambda x:(loads(x[0]),loads(x[1])),self.bdb.items())

	def has_key(self,key):
		return self.bdb.has_key(dumps(key))

	def get(self,key):
		return self[key]

	def update(self,dict):
		for i,j in dict.items(): self[i]=j

class FieldBTree:
	"""This is a specialized version of the BTree class. This version uses type-specific 
	keys, and supports efficient key range extraction. The referenced data is a python list
	of 32-bit integers with no repeats allowed. The purpose of this class is to act as an
	efficient index for records. Each FieldBTree will represent the global index for
	one Field within the database. Valid dey types are:
	"d" - integer keys
	"f" - float keys (64 bit)
	"s" - string keys
	"""
	def __init__(self,name,file=None,keytype="s",dbenv=None,nelem=0):
		global globalenv
		if (not dbenv) : dbenv=globalenv
		self.bdb=db.DB(dbenv)
		if file==None : file=name+".bdb"
#		print "Open: ",file
#		if nelem : self.bdb.set_h_nelem(nelem)					# guess how many elements in a hash
		self.bdb.index_open(file,keytype,name,db.DB_BTREE,db.DB_CREATE)
		self.keytype=keytype
#		self.bdb.open(file,name,db.DB_HASH,db.DB_CREATE)

	def typekey(self,key) :
		if key==None : return None
		if self.keytype=="f" : return float(key)
		if self.keytype=="d" : return int(key)
		return str(key)
			
	def removeref(self,key,item):
		"""The keyed value must be a list of objects. 'item' will be removed from this list"""
		key=self.typekey(key)
		self.bdb.index_remove(key,item)
		
	def addref(self,key,item):
		"""The keyed value must be a list, and is created if nonexistant. 'item' is added to the list. """
		key=self.typekey(key)
		self.bdb.index_append(key,item)

	def __del__(self):
		self.close()

	def close(self):
		self.bdb.close()

	def __len__(self):
		return len(self.bdb)
#		if (self.len<0) : self.keyinit()
#		return self.len

	def __setitem__(self,key,val):
		key=self.typekey(key)
		if (val==None) :
			self.__delitem__(key)
		else : self.bdb.index_put(key,val)

	def __getitem__(self,key):
		key=self.typekey(key)
		return self.bdb.index_get(key)

	def __delitem__(self,key):
		key=self.typekey(key)
		self.bdb.delete(key)

	def __contains__(self,key):
		key=self.typekey(key)
		return self.bdb.index_has_key(key)

	def keys(self,mink=None,maxk=None):
		"""Returns a list of valid keys, mink and maxk allow specification of
		minimum and maximum key values to retrieve"""
		mink=self.typekey(mink)
		maxk=self.typekey(maxk)
		return self.bdb.index_keys(mink,maxk)

	def values(self,mink=None,maxk=None):
		"""Returns a single list containing the concatenation of the lists of,
		all of the individual keys in the mink to maxk range"""
		mink=self.typekey(mink)
		maxk=self.typekey(maxk)
		return self.bdb.index_values(mink,maxk)

	def items(self,mink=None,maxk=None):
		mink=self.typekey(mink)
		maxk=self.typekey(maxk)
		return self.bdb.index_items(mink,maxk)

	def has_key(self,key):
		key=self.typekey(key)
		return self.bdb.index_has_key(key)

	def get(self,key):
		key=self.typekey(key)
		return self[key]

	def update(self,dict):
		self.bdb.index_update(dict)

# vartypes is a dictionary of valid data type names keying a tuple
# with an indexing type and a validation/normalization
# function for each. Currently the validation functions are fairly stupid.
# some types aren't currently indexed, but should be eventually
valid_vartypes={
	"int":("d",lambda x:int(x)),			# 32-bit integer
	"longint":("d",lambda x:int(x)),		# not indexed properly this way
	"float":("f",lambda x:float(x)),		# double precision
	"longfloat":("f",lambda x:float(x)),	# arbitrary precision, limited index precision
	"string":("s",lambda x:str(x)),			# string from an enumerated list
	"text":(None,lambda x:str(x)),			# freeform text, not indexed yet
	"time":("s",lambda x:str(x)),			# HH:MM:SS
	"date":("s",lambda x:str(x)),			# yyyy/mm/dd
	"datetime":("s",lambda x:str(x)),		# yyyy/mm/dd HH:MM:SS
	"intlist":(None,lambda y:map(lambda x:int(x),y)),		# list of integers
	"floatlist":(None,lambda y:map(lambda x:float(x),y)),	# list of floats
	"stringlist":(None,lambda y:map(lambda x:str(x),y)),	# list of enumerated strings
	"url":(None,lambda x:str(x)),			# link to a generic url
	"hdf":(None,lambda x:str(x)),			# url points to an HDF file
	"image":(None,lambda x:str(x)),			# url points to a browser-compatible image
	"binary":lambda x:str(x),				# url points to an arbitrary binary
	"child":lambda y:map(lambda x:int(x),y),	# link to dbid/recid of a child record
	"link":lambda y:map(lambda x:int(x),y)		# lateral link to related record dbid/recid
}

# Valid physical property names
# this really ought to have a list of valid units for each property, and perhaps a conversion
# function of some sort
valid_properties = ["count","length","area","volume","mass","temperature","pH","voltage","current","resistance","inductance",
	"transmittance","absorbance","relative_humidity","velocity","momentum","force","energy","angular_momentum"]

				
class FieldType:
	"""This class defines an individual data Field that may be stored in a Record.
	Field definitions are related in a tree, with arbitrary lateral linkages for
	conceptual relationships. The relationships are handled externally by the
	Database object.""" 
	def __init__(self,creator,name=None,vartype=None,desc_short=None,desc_long=None,property=None,defaultunits=None):
		self.name=name					# This is the name used in XML files to refer to this field, lower case
		self.vartype=vartype			# Variable data type. List of valid types in the module global 'vartypes'
		self.desc_short=desc_short		# This is a very short description for use in forms
		self.desc_long=desc_long		# A complete description of the meaning of this variable
		self.property=property			# Physical property represented by this field, List in 'properties'
		self.defaultunits=defaultunits	# Default units (optional)
		self.creator=creator			# original creator of the record
		self.creationtime=time.strftime("%Y/%m/%d %H:%M:%S")
										# creation date

			
class RecordType:
	"""This class defines a prototype for Database Records. Each Record is a member of
	a RecordClass. This class contains the information giving meaning to the data Fields
	contained by the Record"""
	def __init__(self):
		self.name=None				# the name of the current RecordType, somewhat redundant, since also stored as key for index in Database
		self.mainview=None			# an XML string defining the experiment with embedded fields
									# this is the primary definition of the contents of the record
		self.views={}				# Dictionary of additional (named) views for the record
		self.fields=[]				# A list containing the names of all fields used in any of the views
									# this represents all fields that must be defined to have a complete
									# representation of the record. Note, however, that such completeness
									# is NOT REQUIRED to have a valid Record 

class User:
	"""This defines a database user, note that group 0 membership is required to add new records"""
	def __init__(self):
		self.username=None			# username for logging in, First character must be a letter.
		self.password=None			# sha hashed password
		self.groups=[]				# user group membership
									# magic groups are 0 = add new records, -1 = administrator, -2 = read-only administrator
		self.name=None				# tuple first, last, middle
		self.email=None				# email address
		self.altemail=None			# alternate email
		self.phone=None				# non-validated string
		self.fax=None				#
		self.cellphone=None			#
			
class Context:
	"""Defines a database context (like a session). After a user is authenticated
	a Context is created, and used for subsequent access."""
	def __init__(self,ctxid=None,db=None,user=None,groups=None,host=None,maxidle=1800):
		self.ctxid=ctxid			# unique context id
		self.db=db					# Points to Database object for this context
		self.user=user				# validated username
		self.groups=groups			# groups for this user
		self.host=host				# ip of validated host for this context
		self.time=time.time()		# last access time for this context
		self.maxidle=maxidle
		
class Record:
	"""This class encapsulates a single database record. In a sense this is an instance
	of a particular RecordType, however, note that it is not required to have a value for
	every field described in the RecordType, though this will usually be the case.
	
	To modify the fields in a record use the normal obj[key]= or update() approaches. 
	Changes are not stored in the database until commit() is called. To examine fields, 
	use obj[key]. There are a few special keys, handled differently:
	owner,creator,creationtime,permissions,comments

	Record instances must ONLY be created by the Database class through retrieval or
	creation operations. self.context will store information about security and
	storage for the record.
	
	Mechanisms for changing existing fields are a bit complicated. In a sense, as in a 
	physical lab notebook, an original value can never be changed, only superceded. 
	All records have a 'magic' field called 'comments', which is an extensible array
	of text blocks with immutable entries. 'comments' entries can contain new field
	definitions, which will supercede the original definition as well as any previous
	comments. Changing a field will result in a new comment being automatically generated
	describing and logging the value change.
	
	From a database standpoint, this is rather odd behavior. Such tasks would generally be
	handled with an audit log of some sort. However, in this case, as an electronic
	representation of a Scientific lab notebook, it is absolutely necessary
	that all historical values are permanently preserved for any field, and there is no
	particular reason to store this information in a separate file. Generally speaking,
	such changes should be infrequent.
	
	Naturally, as with anything in Python, anyone with code-level access to the database
	can easily override this behavior by changing 'fields' directly rather than using
	the supplied access methods. There may be appropriate uses for this when constructing
	a new Record before committing changes back to the database.
	"""
	def __init__(self):
		"""Record must be created with a context. This should only be done directly
		by a Database object, to insure security and protocols are handled correctly"""
		self.recid=None				# 32 bit integer recordid (within the current database)
		self.rectype=""				# name of the RecordType represented by this Record
		self.__fields={comments:[]}	# a Dictionary containing field names associated with their data
		self.__ofields={}				# when a field value is changed, the original value is stored here
		self.__owner=0				# The owner of this record
		self.__creator=0			# original creator of the record
		self.__creationtime=None	# creation date
		self.__permissions=((),(),())
									# permissions for read access, comment write access, and full write access
									# each element is a tuple of user names or group id's, if a -3 is present
									# this denotes access by any logged in user, if a -4 is present this
									# denotes anonymous record access
		self.__context=None			# Validated access context
		self.__ptest=[0,0,0,0]		# Results of security test performed when the context is set
									# correspond to, read,comment,write and owner permissions
	
	def __getstate__(self):
		"""the context and other session-specific information should not be pickled"""
		odict = self.__dict__.copy() # copy the dict since we change it
		del odict['__context']
		del odict['__ptest']
		return odict
	
	def __setstate__(self,dict):
		"""restore unpickled values to defaults after unpickling"""
		self.__dict__.update(dict)	
		self.__context=None
		self.__ptest=[0,0,0,0]

	def setContext(self,ctx):
		"""This method may ONLY be used directly by the Database class. Constructing your
		own context will not work"""
		self.__context__=ctx
		if self.__creator==0 :
			self.__owner=ctx.user
			self.__creator=ctx.user
			self.__creationtime=time.strftime("%Y/%m/%d %H:%M:%S")
			self.__permissions=((),(),(ctx.user))
		
		# test for owner access in this context
		if (-1 in ctx.groups or ctx.user==self.owner) : self._ptest=[1,1,1,1]	
		else:
			# we use the sets module to do intersections in group membership
			# note that an empty Set tests false, so u1&p1 will be false if
			# there is no intersection between the 2 sets
			p1=Set(self.__permissions[0]+self.__permissions[1]+self.__permissions[2])
			p2=Set(self.__permissions[1]+self.__permissions[2])
			p3=Set(self.__permissions[2])
			u1=Set(ctx.groups+(-4))				# all users are permitted group -4 access
			
			if ctx.user!=None : u1.add(-3)		# all logged in users are permitted group -3 access
			
			# test for read permission in this context
			if (-2 in u1 or ctx.user in p1 or u1&p1) : self.__ptest[0]=1
	
			# test for comment write permission in this context
			if (ctx.user in p2 or u1&p2): self.__ptest[1]=1
						
			# test for general write permission in this context
			if (ctx.user in p3 or u1&p3) : self.__ptest[2]=1
		return self.__ptest
	
	def __str__(self):
		"A string representation of the record"
		ret=["%d (%s)\n"%(self.recid,self.rectype)]
		for i,j in self.__fields.items:
			ret.append("%12s:  %s\n"%(str(i),str(j)))
		return ret.join()
		
	def __getitem__(self,key):
		"""Behavior is to return None for undefined fields, None is also
		the default value for existant, but undefined fields, which will be
		treated identically"""
		if not self.__ptest[0] : raise SecurityError,"No permission to access record %d"%self.recid
				
		key=key.lower()
		if key=="owner" : return self.__owner
		if key=="creator" : return self.__creator
		if key=="creationtime" : return self.__creationtime
		if key=="permissions" : return self.__permissions
		if self.__fields.has_key(key) : return self.__fields[key]
		return None
	
	def __setitem__(self,key,value):
		"""This and 'update' are the primary mechanisms for modifying the fields in a record
		Changes are not written to the database until the commit() method is called!"""
		# comments may include embedded field values if the user has full write access
		key=key.strip()
		if (key=="comments") :
			if self.__ptest[1]:
				dict=self.parsestring(value)	# find any embedded fields
				if len(dict)>0 and not self.__ptest[2] : 
					raise SecurityError,"Insufficient permission to modify field in comment for record %d"%self.recid
				
				self.__fields["comments"].append((self.__context.user,time.strftime("%Y/%m/%d %H:%M:%S"),value))	# store the comment string itself
				
				# now update the values of any embedded fields
				for i,j in dict.items():
					self.__realsetitem(i,j)
			else :
				raise SecurityError,"Insufficient permission to add comments to record %d"%self.recid
		elif (key=="owner") :
			if self.__ptest[3]: self.__owner=value
			else : raise SecurityError,"Only the administrator or the record owner can change the owner"
		elif (key=="creator" or key=="creationtime") :
			# nobody is allowed to do this
			raise SecurityError,"Creation fields cannot be modified"
		elif (key=="permissions") :
			if self.__ptest[2]:
				try:
					value=(tuple(value[0]),tuple(value[1]),tuple(value[2]))
				except:
					raise TypeError,"Permissions must be a 3-tuple of tuples"
			else: 
				raise SecurityError,"Write permission required to modify security %d"%self.recid
		else :
			if not self.__ptest[2] : raise SecurityError,"No write permission for record %d"%self.recid
			if key in self.__fields :
				self.__fields.comments.append((self.__context.user,time.strftime("%Y/%m/%d %H:%M:%S"),"<field name=%s>%s</field>"%(str(key),str(value))))
			__realsetitem(key,value)
	
	def __realsetitem(self,key,value):
			"""This insures that copies of original values are made when appropriate
			security should be handled by the parent method"""
			if key in self.__fields and not key in self.__ofields : self.__ofields[key]=self.__fields[key]
			self.__fields[key]=value
									

	def parsestring(self,text):
		"""This will exctract XML 'value' tags from a block of text"""
		# This nasty regex will extract <aaa bbb=ccc>ddd</eee> blocks as [(aaa,bbb,ccc,ddd,eee),...]
		srch=re.findall("<([^> ]*) ([^=]*)=([^>]*)>([^<]*)</([^>]*)>" ,text)
		ret={}
		if not srch : return ret
		for t in srch:
			if (t[0].lower!="field" or t[1].lower!="name" or t[4]!="field" or " " in t[2].strip()) :continue
			ret[t[2].strip()]=t[3]
									
	def update(self,dict):
		"""due to the processing required, it's best just to implement this as
		a sequence of calls to the existing setitem method"""
		for i,j in dict.items(): self[i]=j
	
	def keys(self):
		"""All retrievable keys for this record"""
		if not self.__ptest[0] : raise SecurityError,"No permission to access record %d"%self.recid		
		return tuple(self.__fields.keys())+("owner","creator","creationdate","permissions")
		
	def items(self):
		"""Key/value pairs"""
		if not self.__ptest[0] : raise SecurityError,"No permission to access record %d"%self.recid		
		ret=self.__fields.items()
		ret+=[(i,self[i]) for i in ("owner","creator","creationdate","permissions")]

	def has_key(self,key):
		if key in self.keys() or key in ("owner","creator","creationdate","permissions"): return True
		return False

	def commit(self):
		"""This will commit any changes back to permanent storage in the database, until
		this is called, all changes are temporary"""
		self.__context.db.putRecord(self,self.__context.ctxid)
	
#keys(), values(), items(), has_key(), get(), clear(), setdefault(), iterkeys(), itervalues(), iteritems(), pop(), popitem(), copy(), and update()	
class Database:
	"""This class represents the database as a whole. There are 3 primary identifiers used in the database:
	dbid - Database id, a unique identifier for this database server
	recid - Record id, a unique (32 bit int) identifier for a particular record
	ctxid - A key for a database 'context' (also called a session), allows access for pre-authenticated user
	
	TODO : Probably should make more of the member variables private for slightly better security"""
		def __init__(self,path=".",cachesize=256000000,logfile="db.log"):
			self.path=path
			self.logfile=path+"/"+logfile
		
			self.LOG(4,"Database initialization started")
				
			self.__contexts={}			# dictionary of current db contexts, may need to put this on disk for mulithreaded server ?
						
			# This sets up a DB environment, which allows multithreaded access, transactions, etc.
			self.dbenv=db.DBEnv()
			self.dbenv.set_cachesize(0,cachesize,4)		# gbytes, bytes, ncache (splits into groups)
			self.dbenv.set_data_dir(path)
			self.dbenv.open(path+"/home",db.DB_CREATE+db.DB_INIT_MPOOL)
			
			if not os.access(path+"/security",F_OK) : os.mkdirs(path+"/security")
			if not os.access(path+"/index",F_OK) : os.mkdir(path+"/index")
			
			# Users
			self.users=BTree("users",path+"/security/users.bdb",dbenv=self.dbenv)						# active database users
			self.newuserqueue=BTree("newusers",path+"/security/newusers.bdb",dbenv=self.dbenv)			# new users pending approval
			
			# Defined FieldTypes
			self.fieldtypes=BTree("FieldTypes",path+"/FieldTypes.bdb",dbenv=self.dbenv)						# FieldType objects indexed by name

			# Defined RecordTypes
			self.recordtypes=BTree("RecordTypes",path+"/RecordTypes.bdb",dbenv=self.dbenv)					# RecordType objects indexed by name
						
			# The actual database
			self.records=BTree("database",path+"/database.bdb",dbenv=self.dbenv)						# The actual database, containing id referenced Records
			try:
				max=self.records[0]
			except:
				self.records[0]=0
				self.LOG(3,"New database created")
			
			# Indices
			self.secrindex=FieldBTree("secrindex",path+"/security/roindex.bdb","s",dbenv=self.dbenv)	# index of records each user can read
			self.recordtypeindex=FieldBTree("RecordTypeindex",path+"/RecordTypeindex.bdb","s",dbenv=self.dbenv)		# index of records belonging to each RecordType
			self.fieldindex={}				# dictionary of FieldBTrees, 1 per FieldType, not opened until needed

			# The mirror database for storing offsite records
			self.records=BTree("mirrordatabase",path+"/mirrordatabase.bdb",dbenv=self.dbenv)			# The actual database, containing (dbid,recid) referenced Records

			# Workflow database, user indexed list of tuples of things to do
			# TODO:  Clarify this a bit
			self.workflow=BTree("workflow",path+"/workflow.bdb",dbenv=self.dbenv)
						
			self.LOG(4,"Database initialized")
					
		def LOG(self,level,message):
			"""level is an integer describing the seriousness of the error:
			0 - security, security-related messages
			1 - critical, likely to cause a crash
			2 - serious, user will experience problem
			3 - minor, likely to cause minor annoyances
			4 - info, informational only
			5 - verbose, verbose logging """
			global LOGSTRINGS
			if (level<0 or level>5) : level=0
			try:
				o=file(self.logfile,"a")
				o.write("%s: (%s)  %s\n"%(time.ctime(),LOGSTRINGS[level],message))
				o.close()
			except:
				print("Critical error!!! Cannot write log message\n")
										
		def login(self,username="anonymous",password="",host=None,maxidle=1800):
			"""Logs a given user in to the database and returns a ctxid, which can then be used for
			subsequent access"""
			ctx=None
			
			# anonymous user
			if (username=="anonymous" or username=="") :
				ctx=Context(self,None,(),host,maxidle)
			
			# check password, hashed with md5 encryption
			else :
				s=md5.new(password)
				user=self.users[username]
				if (s.hexdigest()==user.password) : ctx=Context(self,username,user.groups,host,maxidle)
				else:
					self.LOG(0,"Invalid password: %s (%s)"%(username,host))
					raise ValueError,"Invalid Password"
			
			# This shouldn't happen
			if ctx==None :
				self.LOG(1,"System ERROR, login(): %s (%s)"%(username,host))
				raise Exception,"System ERROR, login()"
			
			# we use md5 to make a key for the context as well
			s=md5.new(username+str(host)+str(time.time()))
			ctx.ctxid=s.hexdigest()
			self.__contexts[s.hexdigest()]=ctx
			
			return s.hexdigest()

		def cleanupcontexts(self):
			"""This should be run periodically to clean up sessions that have been idle too long"""
			self.lastctxclean=time.time()
			for k in __contexts.items():
				if k[1].time+k[1].maxidle<time.time() : del __contexts[k[0]]
			
		def __getcontext(self,key,host):
			"""Takes a key and returns a context (for internal use only)
			Note that both key and host must match."""
			if (time.time()>self.lastctxclean+30):
				self.cleanupcontexts()		# maybe not the perfect place to do this, but it will have to do
			
			try:
				ctx=__contexts(key)
			except:
				self.LOG(4,"Session expired")
				raise KeyError,"Session expired"
				
			if host!=ctx.host :
				self.LOG(0,"Hacker alert! Attempt to spoof context (%s != %s)"%(host,ctx.host))
				raise Exception,"Bad address match, login sessions cannot be shared"
			
			return ctx			

		def reindex(self,key,oldval,newval,recid)
			"""This function reindexes a single key/value pair
			This includes creating any missing indices if necessary"""

			if (oldval==newval) : return
			try:
				ind=self.fieldindex[key]		# Try to get the index for this key
			except:
				# index not open yet, open/create it
				try:
					f=self.FieldType[key]		# Look up the definition of this field
				except:
					# Undefined field, we can't create it, since we don't know the type
					raise FieldError,"No such field %s defined"%key
				tp=valid_vartypes[f.vartype][0]
				if not tp : return			# if this is None, then this is an 'unindexable' field
				
				# create/open index
				self.fieldindex[key]=FieldBTree(key,"%s/index/%s.bdb"%(self.path,key),tp,self.dbenv)
				ind=self.fieldindex[key]
			
			# remove the old ref and add the new one
			if oldval!=None : ind.removeref(oldval,recid)
			if newval!=None : ind.addref(newval,recid)

		def reindexsec(self,oldlist,newlist,recid):
			"""This updates the security (read-only) index
			takes two lists of userid/groups (may be None)"""
			o=Set(oldlist)
			n=Set(newlist)
			
			uo=o-n	# unique elements in the 'old' list
			un=n-o	# unique elements in the 'new' list

			# anying in both old and new should be ok,
			# So, we remove the index entries for all of the elements in 'old', but not 'new'
			for i in uo:
				self.secrindex.removeref(i,recid)

			# then we add the index entries for all of the elements in 'new', but not 'old'
			for i in un:
				self.secrindex.addred(i,recid)
													
		def putRecord(self,record,ctxid):
			"""The record has everything we need to commit the data. However, to 
			update the indices, we need the original record as well. This also provides
			an opportunity for double-checking security vs. the original"""
			ctx=__getcontext(ctxid)

			try:
				orig=self.records[record.recid]		# get the unmodified record
			except:
				# Record must not exist, lets create it
				#p=record.setContext(ctx)
				user=self.users[ctx.user]
				if (not 0 in user.groups) and (not -1 in user.groups) : raise SecurityError,"No permission to create records"
				
				# index fields
				for k,v in record.items():
					self.reindex(k,None,v,record.recid)
				
				self.reindexsec(None,record["security"],record.recid)		# index security
				self.recordtypeindex.addref(record.rectype,record.recid)	# index recordtype
				return
					
			p=orig.setContext(ctx)				# security check on the original record
			
			# Ok, to efficiently update the indices, we need to figure out what changed
			fields=Set(orig.keys()).union_update(record.keys())		# list of all fields (old and new)
			changedfields=[]
			for f in fields:
				try:
					if (orig[f]!=record[f]) : changedfields.append(f)
				except:
					changedfields.append(f)
			
			if not p[2] :
				if not p[1] : raise SecurityError,"No permission to modify record %d"%record.recid
				if len(changedfields>1) or changedfields[0]!="comments" : raise SecurityError,"Insufficient permission to change field values on record %d"%record.recid
			
			# Now update the indices
			for f in changedfields:
				# reindex will accept None as oldval or newval
				try:    oldval=orig[f]
				except: oldval=None
				
				try:    newval=record[f]
				except: newval=None

				self.reindex(f,oldval,newval,record.recid)

		def newRecord(self,rectype,init):
			"""This will create an empty record and (optionally) initialize it for a given RecordType (which must
			already exist)."""
			ret=Record()
			try:
				t=self.RecordType[rectype]			# try to get the RecordType entry
			except:
				raise Exception,"No such RecordType (%s)"%rectype	
			ret.rectype=rectype						# if we found it, go ahead and set up
			
			ret.recid=self.records[0]+1				# Get a new record-id
			self.records[0]=ret.recid				# Update the recid counter, TODO: do the update more safely/exclusive access
			
			if init:
				for i in t.fields():
					ret[i]=None							# dummy entries for each field
			
			return ret
			
		def getRecord(self,ctxid,recid,dbid=0) :
			"""Primary method for retrieving records. ctxid is mandatory. recid may be a list.
			if dbid is 0, the current database is used."""
			
			ctx=__getcontext(ctxid)
			
			if (dbid!=0) : raise Exception,"External database support not yet available"
			
			# if a single id was requested, return it
			# setContext is required to make the record valid, and returns a binary security tuple
			if (isinstance(recid,int)):
				rec=self.records[recid]
				p=rec.setContext(ctx)
				if p[0] : return rec
				raise Exception,"No permission to access record"
			elif (isinstance(recid,list)):
				rec=map(lambda x:self.records[x],recid)
				for r in rec:
					p=rec.setContext(ctx)
					if not p[0] : raise Exception,"No permission to access one or more records"	
				return rec
			else : raise KeyError,"Invalid Key"
			
		def getRecordSafe(self,ctxid,recid,dbid=0) :
			"""Same as getRecord, but failure will produce None or a filtered list"""
			
			ctx=__getcontext(ctxid)
			
			if (dbid!=0) : return None
			
			if (isinstance(recid,int)):
				try:
					rec=self.records[recid]
				except: 
					return None
				p=rec.setContext(ctx)
				if p[0] : return rec
				return None
			elif (isinstance(recid,list)):
				try:
					rec=map(lambda x:self.records[x],recid)
				except: 
					return None
				rec=filter(lambda x:x.setContext(ctx)[0],rec)
				return rec
			else : return None
			