#!/usr/bin/env python
# $Id$

import sys
import thread
import os.path
import atexit
import multiprocessing
import functools
import contextlib
import threading
import thread
import time

import twisted.internet
import twisted.web.static
import twisted.web.server
import twisted.internet.reactor
import twisted.python.threadpool

import jsonrpc.server

try:
	from twisted.internet import ssl
except ImportError:
	ssl = None

import emen2.web.notifications
import emen2.web.view
import emen2.db.config
config = emen2.db.config.g()

# EMEN2 Resources. To be migrated.
import emen2.web.resource
import emen2.web.resources.jsonrpcresource
# import emen2.web.resources.downloadresource
# import emen2.web.resources.uploadresource
# import emen2.web.resources.xmlrpcresource
# import emen2.web.resources.jsonrpcresource


def addSlash(request):
	# Modified from twisted.web.static
    qs = ''
    qindex = request.uri.find('?')
    if qindex != -1:
        qs = request.uri[qindex:]

    return "%s/%s"%((request.uri.split('?')[0]), qs)


##### Simple DB Pool loosely based on twisted.enterprise.adbapi.ConnectionPool #####		

class DBPool(object):
	running = False
	
	def __init__(self, min=0, max=1):
		# Minimum and maximum number of threads
		self.min = min
		self.max = max
		
		# All connections, hashed by Thread ID
		self.dbs = {}
		
		# Generate Thread ID
		self.threadID = thread.get_ident

		# Connect to reactor
		self.reactor = twisted.internet.reactor
		self.threadpool = twisted.python.threadpool.ThreadPool(self.min, self.max)

	def connect(self):
		tid = self.threadID()
		print '# threads: %s'%len(self.dbs)
		db = self.dbs.get(tid)
		if not db:
			db = emen2.db.opendb()
			self.dbs[tid] = db
		return db

	def disconnect(self, db):
		tid = self.threadID()
		if db is not self.dbs.get(tid):
			raise Exception('Wrong connection for thread')
		if db:
			# db.close
			del self.dbs[tid]

	def rundb(self, call, *args, **kwargs):
		return twisted.internet.threads.deferToThread(self._rundb, call, *args, **kwargs)

	def _rundb(self, call, *args, **kwargs):
		db = self.connect()
		result = call(db=db, *args, **kwargs)
		return result

	def runtxn(self, call, *args, **kwargs):
		return twisted.internet.threads.deferToThread(self._runtxn, call, *args, **kwargs)
	
	def _runtxn(self, call, *args, **kwargs):
		db = self.connect()
		with db:
			result = call(db=db, *args, **kwargs)
		return result

		

##### pool and reactor #####

pool = DBPool()
reactor = twisted.internet.reactor		

##### Test Resource #####

class TestResource(object):
	# The Resource specification for leaf nodes 
	# only requires render() and isLeaf = True
	isLeaf = True

	def render(self, request):
		# print "Render: %s"%request.path		
		deferred = pool.runtxn(self.render_action, args=request.args)
		deferred.addCallback(self.render_cb, request)
		deferred.addErrback(self.render_eb, request)
		request.notifyFinish().addErrback(self._request_broken, request, deferred)		
		return twisted.web.static.server.NOT_DONE_YET			
		
	def render_action(self, *args, **kwargs):
		result = '%s %s %s'%(time.strftime('%Y/%m/%d %H:%M:%S'), args, kwargs)
		return result
		
	def render_cb(self, result, request):
		# print "Callback"
		request.write(result)
		request.finish()
	
	def render_eb(self, failure, request):
		# print "Failure:", failure
		request.write('failure!')
		request.finish()	

	def _request_broken(self, failure, request, deferred):
		# The errback will be called, but not the callback.
		deferred.cancel()

		


##### Routing Resource #####

class Router(twisted.web.resource.Resource):
	isLeaf = False

	# Find a resource or view
	def getChildWithDefault(self, path, request):
		if path in self.children:
			return self.children[path]

		path = request.path
		if not path:
			path = '/'
		if path[-1] != "/":
			path = "%s/"%path
		request.path = path
		
		try:
			view, method = emen2.web.routing.resolve(path=request.path)
		except:
			return self
			
		# This may move into routing.Router in the future.
		view = view()
		view.render = functools.partial(view.render, method=method)
		return view
		

	# Resource was not found
	def render(self, request):
		return 'Not found'
	
		

class EMEN2Server(object):
	# Use HTTPS?
	EMEN2HTTPS = False # config.claim('network.EMEN2HTTPS', False, lambda v: isinstance(v, bool))

	# Which port to receive HTTPS request?
	EMEN2PORT_HTTPS = 436 # config.claim('network.EMEN2PORT_HTTPS', 443, lambda v: isinstance(v, (int,long)))

	# How many threads to load, defaults to :py:func:`multiprocessing.cpu_count`+1
	NUMTHREADS = 1 # config.claim('network.NUMTHREADS', multiprocessing.cpu_count()+1, lambda v: (v < (multiprocessing.cpu_count()*2)) )

	# Which port to listen on
	PORT = 8080 # config.watch('network.EMEN2PORT', 8080)

	# Where to find the SSL info
	SSLPATH = '' # config.claim('paths.SSLPATH', '', validator=lambda v: isinstance(v, (str, unicode)))

	def __init__(self, port=None, dbo=None):
		# Configuration options
		self.dbo = dbo or emen2.db.config.DBOptions()
		self.dbo.add_option('--port', type="int", help="Web server port")
		self.dbo.add_option('--https', action="store_true", help="Use HTTPS")
		self.dbo.add_option('--httpsport', type="int", help="HTTPS Port")
		(self.options, self.args) = self.dbo.parse_args()

		# Update the configuration
		if self.options.port or port:
			config.EMEN2PORT = self.options.port or port

		if self.options.https:
			self.EMEN2HTTPS = self.options.https

		if self.options.httpsport:
			self.EMEN2PORT_HTTPS = self.options.httpsport


	@contextlib.contextmanager
	def start(self):
		'''Run the server main loop'''
		config.info('starting EMEN2 version: %s' % emen2.db.config.CVars.version)

		# Routing resource. This will look up request.uri in the routing table
		# and return View resources.
		root = Router()
		yield self, root

		# These resources will be migrated to EMEN2Resources 
		# root.putChild('jsonrpc', jsonrpc.server.JSON_RPC().customize(emen2.web.resources.jsonrpcresource.e2jsonrpc))
		root.putChild('static', twisted.web.static.File(emen2.db.config.get_filename('emen2', 'web/static')))
		root.putChild('static-%s'%emen2.db.config.CVars.version, twisted.web.static.File(emen2.db.config.get_filename('emen2', 'web/static')))
		root.putChild('favicon.ico', twisted.web.static.File(emen2.db.config.get_filename('emen2', 'web/static/favicon.ico')))
		root.putChild('robots.txt', twisted.web.static.File(emen2.db.config.get_filename('emen2', 'web/static/robots.txt')))

		# The Twisted Web server protocol factory,
		#  with our Routing resource as root
		site = twisted.web.server.Site(root)
		
		# Setup the Twisted reactor to listen on web port
		reactor.listenTCP(self.PORT, site)

		# Setup the Twisted reactor to listen on the SSL port
		if self.EMEN2HTTPS and ssl:
			reactor.listenSSL(
				self.EMEN2PORT_HTTPS,
				site,
				ssl.DefaultOpenSSLContextFactory(
					os.path.join(self.SSLPATH, "server.key"),
					os.path.join(self.SSLPATH, "server.crt")
					))

		# config._locked = True
		reactor.run()


def start_emen2():
	# Start the EMEN2Server and load the View resources
	with EMEN2Server().start() as (server, root):
		vl = emen2.web.view.ViewLoader()
		vl.load_extensions()


if __name__ == "__main__":
	start_emen2()


__version__ = "$Revision$".split(":")[1][:-1].strip()