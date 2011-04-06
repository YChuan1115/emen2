# $Id$

from __future__ import with_statement

import os
import sys
import time
import collections
import traceback
import weakref
import functools


import emen2.db.config
g = emen2.db.config.g()

import emen2.db.vartypes
import emen2.db.macros
import emen2.db.properties


# Warning: This module is very sensitive to changes. Please test thoroughly before committing!!


def publicmethod(*args, **kwargs):
	"""Decorator for public admin API database method"""
	def _inner(func):
		emen2.db.proxy.DBProxy._register_publicmethod(func, *args, **kwargs)
		return func
	return _inner





class MethodUtil(object):
	allmethods = set(['doc'])
	def help(self, func, *args, **kwargs):
		return func.__doc__



strht = lambda s, c: s.partition(c)[::2]
def fb(): return 'hi'
def help(mt):
	def _inner(*a, **b):
		return dict(
			doc = getattr(mt, 'doc', None),
			methods = mt.children.keys()
		)
	return _inner

class MethodTree(object):
	class _cursor(object):
		def __init__(self, mt, path = None):
			self.path = path or []
			self.mt = mt
		def __call__(self, *a, **kw):
			meth = self.mt.get_method('.'.join(self.path))
			self.path = []
			return meth(*a, **kw)
		def __getattr__(self, name):
			return type(self)(self.mt, self.path + [name])

	def __init__(self, func=None):
		self.func = func
		if func: self.doc = func.__doc__ or ''
		else: self.doc = ''
		self.children = {}
		self.aliases = {}

	def alias(self, orig, new):
		self.aliases[orig] = new
	def get_alias(self, txt):
		return self.aliases.get(txt,txt)

	def __enter__(self, *a):
		return self._cursor(self)
	def __exit__(self, *a, **kw): pass

	def __call__(self, *a, **kw):
		return self.func(*a, **kw)

	def __getattr__(self, name):
		name = name.replace('_', '.')
		return self.get_method(name)

	def add_method(self, name, func):
		head, tail = strht(name, '.')
		#print head, tail
		if head in self.children:
			self.children[head].add_method(tail, func)
		else:
			if tail != '':
				self.children[head] = MethodTree()
				self.children[head].add_method(tail, func)
			else:
				self.children[name] = MethodTree(func)

	def get_method(self, name):
		name = self.get_alias(name)
		head, tail = strht(name, '.')
		child = self.children.get(head, self)
		if tail == 'help' or head == 'help': child = MethodTree(help(child))
		elif tail == 'writep': child = MethodTree(
			(lambda child: ( # make closure to localize child
					lambda *a, **kw: child.func.write
				)
			)(child)
		)
		elif tail != '' and child is not self: child = child.get_method(tail)
		return child






class _Method(object):
	# Taken from XML-RPC lib to support nested methods
	def __init__(self, proxy, name):
		self._proxy = proxy
		self._name = name


	def __getattr__(self, name):
		func = self._proxy._publicmethods.get("%s.%s"%(self._name, name))
		if func:
			return self._proxy._wrap(func)
		return _Method(self._proxy, "%s.%s" % (self._name, name))


	def __call__(self, *args):
		raise AttributeError, "No public method %s"%self._name



class DBProxy(object):
	"""A proxy that provides access to database public methods and handles low level details, such as Context and transactions.

	db = DBProxy()
	db._login(username, password)

	"""

	_publicmethods = {}
	mt = MethodTree()

	@classmethod
	def _allmethods(cls):
		return set(cls._publicmethods)

	def _get_publicmethods(self):
		result = {}
		for x in self._publicmethods:
			cur = result
			for y in x.split('.'):
				ncur = cur.get(y, {})
				if ncur is not cur: cur[y] = ncur
				cur = ncur
		return result



	def __init__(self, db=None, ctxid=None, host=None, ctx=None, txn=None):
		# it can cause circular imports if this is at the top level of the module
		import database

		self._txn = None
		self._is_bound = False

		if not db:
			db = database.DB()

		self._db = db
		self._ctx = ctx
		self._txn = txn


	# Implements "with" interface
	def __enter__(self):
		self._starttxn()
		return self


	def __exit__(self, type, value, traceback):
		if type is None:
			self._committxn()
		else:
			# g.log_error('DBProxy.__exit__: type=%s, value=%s, traceback=%s' % (type, value, traceback))
			self._aborttxn()
		self._txn = None


	# Transactions
	def _gettxn(self):
		return self._txn


	def _settxn(self, txn=None):
		self._txn = txn


	def _starttxn(self, write=False):
		self._txn = self._db.txncheck(txn=self._txn, ctx=self._ctx, write=write)
		return self


	def _committxn(self):
		self._txn = self._db.txncommit(txn=self._txn)


	def _aborttxn(self):
		self._txn = self._db.txnabort(txn=self._txn)


	# Rebind a new Context
	def _setContext(self, ctxid=None, host=None):
		try:
			self._ctx = self._db._getcontext(ctxid=ctxid, host=host, txn=self._txn)
			self._ctx.setdb(db=self)
		except:
			self._ctx = None
			raise

		self._is_bound = True
		return self


	def _clearcontext(self):
		if self._is_bound:
			self._ctx = None
			self._bound = False


	def _getctx(self):
		return self._ctx


	@property
	def _bound():
		return self._is_bound


	@_bound.deleter
	def _bound():
		self._clearcontext()


	def _ismethod(self, name):
		if name in self._allmethods(): return True
		return False


	@classmethod
	def _register_publicmethod(cls, func, apiname, write=False, admin=False, ext=False):
		# print "Registering func: %s"%apiname
		# if set([func.apiname, func.func_name]) & cls._allmethods():
		# 	raise ValueError('''method %s already registered''' % name)
		setattr(func, 'apiname', apiname)
		setattr(func, 'write', write)
		setattr(func, 'admin', admin)
		setattr(func, 'ext', ext)


		cls._publicmethods[func.apiname] = func
		cls._publicmethods[func.func_name] = func

		cls.mt.add_method(apiname, func)
		cls.mt.alias(func.func_name, apiname)


	def _checkwrite(self, method):
		return getattr(self.mt.get_method(method).func, "write", False)


	def _callmethod(self, method, args=(), kwargs={}):
		"""Call a method by name with args and kwargs (e.g. RPC access)"""
		#return getattr(self, method)(*args, **kwargs)
		m = self.mt.get_method(method).func
		if m:
			return self._wrap(m)(*args, **kwargs)



	def __getattr__(self, name):
		func = self._publicmethods.get(name)
		if func: return self._wrap(func)
		return _Method(self, name)



	def _wrap(self, func):
		# print "going into wrapper for func: %s / %s"%(func.func_name, func.apiname)
		kwargs = dict(ctx=self._ctx, txn=self._txn)

		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			# t = time.time()
			result = None
			commit = False
			ctx = self._ctx
			kwargs['ctx'] = ctx

			if getattr(func, 'admin', False) and not ctx.checkadmin():
				raise Exception, "This method requires administrator level access."

			self._starttxn()
			kwargs['txn'] = self._txn
			try:
				ctx.setdb(self)
			except:
				pass

			if getattr(func, 'ext', False):
				kwargs['db'] = self._db

			# print 'func: %r, args: %r, kwargs: %r'%(func, args, kwargs)

			try:
				# result = func.execute(*args, **kwargs)
				result = func(self._db, *args, **kwargs)

			except Exception, e:
				# traceback.print_exc(e)
				if commit is True:
					txn and self._db.txnabort(ctx=ctx, txn=txn)
				raise

			else:
				if commit is True:
					txn and self._db.txncommit(ctx=ctx, txn=txn)

			# timer!
			# print "---\t\t%10d ms: %s"%((time.time()-t)*1000, func.func_name)
			return result

		return wrapper


__version__ = "$Revision$".split(":")[1][:-1].strip()
