import operator

import emen2.db.datatypes
import emen2.db.config
g = emen2.db.config.g()


# Convenience
Macro = emen2.db.datatypes.Macro



# ian: todo: Macros can specify a return vartype, which will go through normal rendering... 

class macro_recid(Macro):
	"""recid macro"""
	__metaclass__ = Macro.register_view
	def process(self, engine, macro, params, rec, db):
		return rec.recid

	def macroname_render(self, macro, params, rec, mode="unicode", db=None):
		return "Record ID"



class macro_recname(Macro):
	"""recname macro"""
	__metaclass__ = Macro.register_view
			
	def process(self, engine, macro, params, rec, db):
		return db.renderview(rec, viewtype="recname")

	def macroname_render(self, macro, params, rec, mode="unicode", db=None):
		return "Record ID"				
				


class macro_childcount(Macro):
	"""childcount macro"""
	__metaclass__ = Macro.register_view
	
	def preprocess(self, engine, macro, params, recs, db):
		rectypes = params.split(",")
		children = db.getchildren([rec.recid for rec in recs], rectype=rectypes, recurse=3)
		for rec in recs:
			key = engine.get_cache_key('getchildren', rec.recid, *rectypes)
			engine.store(key, len(children.get(rec.recid,[])))

		
	def process(self, engine, macro, params, rec, db):
		"""Now even more optimized!"""
		rectypes = params.split(",")
		key = engine.get_cache_key('getchildren', rec.recid, *rectypes)
		hit, children = engine.check_cache(key)
		if not hit:
			children = len(db.getchildren(rec.recid, rectype=rectypes, recurse=3))
			engine.store(key, children)

		return children


	def macroname_render(self, macro, params, rec, mode="unicode", db=None):
		return "Childcount: %s"%(params)




class macro_img(Macro):
	"""image macro"""
	__metaclass__ = Macro.register_view

	def process(self, engine, macro, params, rec, db):
		default=["file_binary_image","640","640"]
		try:
			ps=params.split(" ")
		except:
			return "(Image Error)"
		for i,v in list(enumerate(ps))[:3]:
			default[i]=v
		param,width,height=default

		try:	
			pd=db.getparamdef(param)
		except:
			return "(Unknown parameter)"

		if pd.vartype=="binary":
			bdos=rec[param]
		elif pd.vartype=="binaryimage":
			bdos=[rec[param]]
		else:
			return "(Invalid parameter)"

		#print bdos
		if bdos==None:
			return "(No Image)"

		ret=[]
		for i in bdos:
			try:
				bdoo = db.getbinary(i, filt=False)
				fname = bdoo.get("filename")
				bname = bdoo.get("filepath")
				lrecid = bdoo.get("recid")
				ret.append('<img src="%s/download/%s/%s" style="max-height:%spx;max-width:%spx;" />'%(g.EMEN2WEBROOT,i[4:],fname,height,width))
			except:
				ret.append("(Error: %s)"%i)

		return "".join(ret)


	def macroname_render(self, macro, params, rec, mode="unicode", db=None):
		return "Image Macro"



class macro_childvalue(Macro):
	"""childvalue macro"""
	__metaclass__ = Macro.register_view

	def process(self, engine, macro, params, rec, db):
		recid = rec.recid
		children = db.getrecord(db.getchildren(recid))
		return [i.get(params) for i in children]


	def macroname_render(self, macro, params, rec, mode="unicode", db=None):
		return "Child Value: %s"%params



class macro_parentvalue(Macro):
	"""parentvalue macro"""
	__metaclass__ = Macro.register_view
	
		
	def process(self, engine, macro, params, rec, db):
		#print db, host
		recid = rec.recid
# 		parents = db.getrecord(db.getparents(recid), filt=1)
# 		return filter(lambda x:x, [i.get(params) for i in parents])
		parents = db.getrecord(db.getparents(recid))
		return filter(None, [i.get(params) for i in parents])

	def macroname_render(self, macro, params, rec, mode="unicode", db=None):
		return "Parent Value: %s"%params

	def render_unicode(self, engine, value, macro, params, rec, db):
		return ",".join([unicode(j) for j in value])
		#return ",".join(value)



import cgi
class macro_escape_paramdef_val(Macro):
	"""escape_paramdef_val macro"""
	__metaclass__ = Macro.register_view
		
	def process(self, engine, macro, params, rec, db):
		return cgi.escape(rec.get(params, ''))

	def macroname_render(self, macro, params, rec, mode="unicode", db=None):
		return "Escaped Value: %s"%params



class macro_renderchildren(Macro):
	"""renderchildren macro"""
	__metaclass__ = Macro.register_view
		
	def process(self, engine, macro, params, rec, db):
		return db.renderview(db.getchildren(params), viewtype=params or "recname") #ian:mustfix

	def macroname_render(self, macro, params, rec, mode="unicode", db=None):
		return "renderchildren"			



class macro_renderchild(Macro):
	"""renderchild macro"""
	__metaclass__ = Macro.register_view
	
		
	def process(self, engine, macro, params, rec, db):
		#rinfo = dict(,host=host)
		#view, key, value = args.split(' ')
		#def get_records(recid):
		#	return db.getindexbyvalue(key.encode('utf-8'), value, **rinfo).intersection(db.getchildren(recid, **rinfo))
		#return render_records(db, rec, view, get_records,rinfo, html_join_func)
		return ""

		
	def macroname_render(self, macro, params, rec, mode="unicode", db=None):
		return "renderchild"		



class macro_renderchildrenoftype(Macro):
	"""renderchildrenoftype macro"""
	__metaclass__ = Macro.register_view

		
	def process(self, engine, macro, params, rec, db):
		# print macro, params
		r = db.renderview(db.getchildren(rec.recid, rectype=params), viewtype="recname")
		hrefs = []
		for k,v in sorted(r.items(), key=operator.itemgetter(1)):
			l = """<li><a href="%s/db/record/%s">%s</a></li>"""%(g.EMEN2WEBROOT, k, v or k)
			hrefs.append(l)
		return "<ul>%s</ul>"%("\n".join(hrefs))


		
	def macroname_render(self, macro, params, rec, mode="unicode", db=None):
		return "renderchildrenoftype"	




class macro_getfilenames(Macro):
	"""getfilenames macro"""
	__metaclass__ = Macro.register_view

		
	def process(self, engine, macro, params, rec, db):
		# files = {}
		# if rec["file_binary"] or rec["file_binary_image"]:
		# 	bids = []
		# 	if rec["file_binary"]:
		# 		bids += rec["file_binary"]
		# 	if rec["file_binary_image"]:
		# 		bids += [rec["file_binary_image"]]
		#
		# 	for bid in bids:
		# 		bid = bid[4:]
		# 		try:
		# 			bname,ipath,bdocounter=db.getbinary(bid,,host=host)
		# 		except Exception, inst:
		# 			bname="Attachment error: %s"%bid
		# 		files[bid]=bname
		#
		# return files
		return ""

		
	def macroname_render(self, macro, params, rec, mode="unicode", db=None):
		return "getfilenames"	




class macro_getrectypesiblings(Macro):
	"""getrectypesiblings macro"""
	__metaclass__ = Macro.register_view

	
		
	def process(self, engine, macro, params, rec, db):
		pass
		# """returns siblings and cousins of same rectype"""
		# ret = {}
		# parents = db.getparents(rec.recid,,host=host)
		# siblings = set()
		#
		# for i in parents:
		# 	siblings = siblings.union(db.getchildren(i))
		#
		# groups = db.groupbyrecorddef(siblings)
		#
		# if groups.has_key(rec.rectype):
		# 	q = db.getindexdictbyvaluefast(groups[rec.rectype],"modifytime")
		# 	ret = [i[0] for i in sorted(q.items(), key=itemgetter(1), reverse=True)] #BUG: What is supposed to happen here?
		#
		
	def macroname_render(self, macro, params, rec, mode="unicode", db=None):
		return "getrectypesiblings"	
		
		
		
		



class macro_thumbnail(Macro):
	"""tile thumb macro"""
	__metaclass__ = Macro.register_view
	
		
	def process(self, engine, macro, params, rec, db):
		format = "jpg"
		defaults = ["file_binary_image", "thumb", "jpg"]
		params = ",".split(params)
		for i,v in enumerate(params):
			defaults[i]=v
		
		bdos = rec.get(defaults[0])
		if not hasattr(bdos,"__iter__"):
			bdos = [bdos]
		return "".join(['<img src="%s/download/%s/%s.%s.%s?size=%s&format=%s" alt="thumbnail" />'%(g.EMEN2WEBROOT, bid, bid, defaults[1], defaults[2], defaults[1], defaults[2]) for bid in filter(lambda x:isinstance(x,basestring), bdos)])


	def macroname_render(self, macro, params, rec, mode="unicode", db=None):
		return "Thumbnail Image"



