"""Various helper functions for sorting, filtering, transforming data, etc."""
import collections
import itertools
from UserDict import DictMixin
from functools import partial

# Temporary fix --
import jsonrpc.jsonutil
def jsonencode(*args, **kwargs):
    """Safer JSON encoding."""
    return jsonrpc.jsonutil.encode(*args, **kwargs).replace('/', r'\/')

def first_or_none(items):
    """Return the first item from a list, or None."""
    items = items or []
    result = None
    if len(items) > 0:
        if hasattr(items, 'keys'):
            result = items.get(first_or_none(items.keys()))
        else:
            result = iter(items).next()
    return result

filter_none = lambda x:x or x==0
def check_iterable(value):
    """Check if a value is iterable; if not, return [value]. Removes None values."""
    if not hasattr(value,"__iter__"):
        value = [value]
    return filter(filter_none, value)

def chunk(l, count=1000):
    """Chunk a list into segments of length count"""
    ll = list(l)
    return (ll[i:i+count] for i in xrange(0, len(ll), count))

def groupchunk(list_, grouper=lambda x: x[0]==x[1], itemgetter=lambda x:x):
    """Groups items in list as long as the grouper function returns True

    >>> chunk([1,3,2,4,3,2,4,5,3,1,43,2,1,1])
    [[1], [3], [2], [4], [3], [2], [4], [5], [3], [1], [43], [2], [1, 1]]
    >>> chunk([1,3,2,4,3,2,4,5,3,1,43,2,1,1], lambda x: x[0]<x[1])
    [[1, 3], [2, 4], [3], [2, 4, 5], [3], [1, 43], [2], [1], [1]]
    """
    if hasattr(list_, '__iter__') and not isinstance(list_, list):
        list_ = list(list_)
    result = [[list_[0]]]
    for x in xrange(len(list_)-1):
        window = list_[x:x+2]
        if not grouper(window):
            result.append([])
        result[-1].append(itemgetter(window[1]))
    return result

def typepartition(names, *types):
    """Partition objects by type.
    
    >>> typepartition([1,'a'], int, str)
    [[1], ['a']]
    """
    ret = collections.defaultdict(list)
    other = list()
    for name in names:
        found = False
        for t in types:
            if isinstance(name, t):
                found = True
                ret[t].append(name)
        if not found:
            other.append(name)

    return [ret.get(t, []) for t in types]+[other]

def dictbykey(l, key='name'):
    """Take a list of items, return a dict keyed by the specified key."""
    return dict((i.get(key), i) for i in l)

def groupbykey(l, key, dtype=None):
    """Take a list of items, return a dict of the items grouped by the specified key."""
    dtype = dtype or list
    d = collections.defaultdict(dtype)
    for i in l:
        k = i.get(key)
        d[k] = adjust(d[k], i)
    return dict(d)

# From database
def tolist(d, dtype=None):
    return oltolist(d, dtype=dtype)[1]

def oltolist(d, dtype=None):
    dtype = dtype or list
    ol = False
    result = None
    if isinstance(d, dtype): 
        pass
    elif isinstance(d, (dict, DictMixin)) or not hasattr(d, "__iter__"):
        d = [d]
        ol = True
    if not isinstance(d, dtype):
        d = dtype(d)
    return ol, d
