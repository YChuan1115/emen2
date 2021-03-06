import datetime
import dateutil
import dateutil.parser
import dateutil.tz

tzutc = dateutil.tz.tzutc()
tzlocal = dateutil.tz.gettz()
default = datetime.datetime(2011, 1, 1)
mintime = datetime.datetime(2000, 1, 1)

import emen2.db
db = emen2.db.opendb(admin=True)

def parseutc(d):
    try:
        t = dateutil.parser.parse(d, default=default)
    except ValueError, e:
        print "Could not parse:", d, e
        return
    if not t.tzinfo:
        t = t.replace(tzinfo=tzlocal)
    t = t.astimezone(tzutc)
    # print "Converted to UTC       :", t.isoformat(), "\t\t", d    
    return t.isoformat()

def parselocal(d):
    try:
        t = dateutil.parser.parse(d, default=default)
    except ValueError, e:
        print "Could not parse:", d, e
        return
    if not t.tzinfo:
        t = t.replace(tzinfo=tzlocal)
    # print "Converted to UTC+offset:", t.isoformat(), "\t\t", d    
    return t.isoformat()

    # t = dateutil.parser.parse(d, default=default).replace(tzinfo=tzlocal)
    # print "Converted to UTC+offset:", t.isoformat(), "\t\t", d
    # return t.isoformat()


def updatebt(btree, ctx, txn):
    for name, item in btree.items(txn=txn, ctx=ctx):
        # print name
        ct = item.__dict__.get('creationtime') or '2001/01/01'
        item.__dict__['creationtime'] = parseutc(ct)
        item.__dict__['modifytime'] = parseutc(item.get('modifytime') or ct)
        btree._put_data(item.name, item, txn=txn)
    btree.rebuild_indexes(ctx=ctx, txn=txn)
    
def updaterecs(ctx, txn):
    # for name in range(550000):
    for count, name in enumerate(db._db["record"].keys(txn=txn)):
        if count % 1000 == 0:
            print name

        rec = db.getrecord(name)
        if not rec:
            continue
            
        ct = rec.__dict__['creationtime']
        rec.__dict__['creationtime'] = parseutc(ct)
        rec.__dict__['modifytime'] = parseutc(rec.get('modifytime') or ct)

        newcomments = []
        for i in rec.__dict__['comments']:
            newcomments.append([i[0], parseutc(i[1]), i[2]])
        rec.__dict__['comments'] = newcomments
        
        newhistory = []
        for i in rec.__dict__['history']:
            newhistory.append([i[0], parseutc(i[1]), i[2], i[3]])
        rec.__dict__['history'] = newhistory
        
        for p in pds:
            if rec.params.get(p):
                rec.params[p] = parselocal(rec.params[p])

        db._db["record"]._put_data(rec.name, rec, txn=txn)
    db._db['record'].rebuild_indexes(ctx=ctx, txn=txn)
    
    
with db:    
    pds = set(db.query([['vartype','==','datetime']], keytype='paramdef', count=0)['names'])
    pds -= set(['creationtime', 'modifytime'])
    print "Converting timestamps for:", pds
        
    ctx = db._ctx
    txn = db._txn
    for i in ['user', 'group', 'paramdef', 'recorddef', 'binary']:
        updatebt(db._db[i], ctx=ctx, txn=txn)
    
    updaterecs(ctx=ctx, txn=txn)
    
        
        
