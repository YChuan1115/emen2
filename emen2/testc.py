import getpass
import atexit
import emen2.globalns
from emen2.config.config import g, DBOptions
parser = DBOptions()
parser.parse_args()

import emen2.Database.DBProxy
import emen2.Database.database

#@atexit.register
def _atexit():
	global db
	try:
		if (raw_input('commit txn [y/N]? ') or 'n').lower().startswith('y'):
			db._committxn()
		else:
			db._aborttxn()
	except NameError,e:
		print e


db = emen2.Database.DBProxy.DBProxy()
ddb = db._DBProxy__db

db._login("root", getpass.getpass())
db._starttxn()
txn = db._gettxn()
ctx = db._getctx()
