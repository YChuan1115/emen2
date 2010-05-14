from emen2.util import db_manipulation
from itertools import chain
import operator

import emen2.Database.globalns
g = emen2.Database.globalns.GlobalNamespace()

class DBQuery(object):
	def __init__(self, db):
		self.db = db
		self.__data = None
		self.__ops = []
		self.__dirty = False

	def __lshift__(self, other):
		if hasattr(other, '__iter__'):
			self.__ops.append(iter(other))
		else:
			self.__ops.append(other.act)
		self.__dirty = True
		return self

	def __repr__(self):
		return "DBQuery(%s, cache_dirty=%s)" % (self.__data, self.__dirty)

	def get_result(self):
		if self.__dirty or self.__data == None:
			data = self.__data or set()
			for op in self.__ops:
				if hasattr(op, '__iter__'):
					data = chain(data, op)
				else:
					data = op(data, self.db)
			self.__ops = []
			self.__data = data
			self.__dirty = False
		return list(self.__data)
	result = property(get_result)

	def reset(self):
		self.__ops = []
		self.__data = None
		self.__dirty = False

class BoolOp(object):
	def __init__(self, op, *args):
		self.__ops = args
		self.__op = op
	def act(self, data, db):
		results = set()
		q = DBQuery(db)
		for item in self.__ops:
			for pred in item:
				q << pred
			results = self.__op(results, set(q.result))
			q.reset()
		for item in results:
			yield item


class Union(BoolOp):
	def __init__(self, *args):
		BoolOp.__init__(self, operator.or_, *args)

class Intersection(BoolOp):
	def __init__(self, *args):
		BoolOp.__init__(self, operator.and_, *args)


class GetRecord(object):
	def act(self, data, db):
		for recid in data:
			yield db.getrecord(recid)

class GetRecordDef(object):
	def act(self, data, db):
		for name in data:
			yield db.getrecorddef(name)

class GetChildren(object):
	def act(self, data, db):
		for recid in data:
			for child in db.getchildren(recid):
				yield child

class GetParents(object):
	def act(self, data, db):
		for recid in data:
			for child in db.getparents(recid):
				yield child

class ParamValue(object):
	def __init__(self, param_name=None):
		self.param_name = param_name
	def act(self, data, db):
		for val in data:
			res = db.getparamvalue(self.param_name, val)
			if bool(res) == True:
				yield res
			else:
				yield None

class FilterByRecordDef(object):
	def __init__(self, recorddefs):
		if hasattr(recorddefs, '__iter__'):
			self.recorddefs = recorddefs
		else:
			self.recorddefs = [recorddefs]
	def act(self, data, db):
		result = set([])
		for name in self.recorddefs:
			result.update(db.getindexbyrecorddef(name))
		if data:
			result = ( set(result) & set(data) ) or result

		for item in result:
			yield item

class FilterByContext(object):
	def act(self, data, db):
		if data:
			result = ( set(data) & set(db.getindexbycontext(ctxid=ctxid, host=host)) ) or data
		else:
			result = db.getindexbycontext(ctxid=ctxid, host=host)

		for item in result:
			yield item

class FilterByValue(object):
	def __init__(self, param_name, value):
		self.param_name = param_name
		self.value = value
	def act(self, data, db):
		if data:
			result = ( set(data) & set(db.getindexbyvalue(self.param_name, self.value)) ) or data
		else:
			result = db.getindexbyvalue(self.param_name, self.value)

		for item in result:
			yield item

class FilterByParamDef(object):
	def __init__(self, param_name):
		self.param_name = param_name
	def act(self, data, db):
		data = db.getrecord(data)
		for x  in data:
			if x[self.param_name] != None:
				yield x.recid

class FilterByParentType(object):
	def __init__(self, recorddef):
		self.recorddef = recorddef
	def act(self, data, db):
		queryset = [ (x, db.getparents(x)) for x in data ]
		for rec, parents in queryset:
			parents = db.groupbyrecorddef(parents)
			if parents.get(self.recorddef, False) != False:
				yield rec

class GetPath(object):
	def act(self, data, db):
		result = db_manipulation.DBTree(db).get_path_id(list(data))
		if not hasattr(result, '__iter__'):
			result = [result]
		for x in result:
			yield x

class GetRoot(object):
	def act(self, data, db):
		yield db_manipulation.DBTree(db).root

class Filter(object):
	def __init__(self, func):
		self.func = func
	def act(self, data, db):
		for x in data:
			if self.func(x):
				yield x

class Map(object):
	def __init__(self, func):
		self.func = func
	def act(self, data, db):
		for x in data:
			yield self.func(x)

class Select(object):
	def __init__(self, **kwargs):
		self.__args = kwargs
	def act(self, data, db):
		data = set(data or [])
		for paramdef, value in self.__args.items():
			data = FilterByValue(paramdef, value).act(data, db)
		for x in data:
			yield x

class EditRecord(object):
	def __init__(self, changes):
		'''
		Edit a records contents.

		@param changes: A dictionary of paramdef:value pairs
		'''
		self.__changes = changes
	def act(self, data, db):
		'''data should be a sequence of records'''
		for rec in data:
			rec.update(self.__changes)
			yield rec

class Commit(object):
	def act(self, data, db):
		for rec in data:
			db.puterecord(rec)
			yield rec

class Unlink(object):
	def __init__(self, parent):
		self.__pid = parent
	def act(self, data, db):
		for rec in data:
			if hasattr(rec, 'recid'):
				id = rec.recid
			else:
				id = int(rec)
			db.pcunlink(self.__pid, id)
			yield rec

class TryGet(object):
	def act(self, data, db):
		for rec in data:
			yield db.trygetrecord(rec)
