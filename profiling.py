from __future__ import division
import numpy as np
from functools import wraps
from time import time
from collections import defaultdict
import inspect

_timings = defaultdict(list)

def profiled(func):
    mod = inspect.getmodule(func)
    if hasattr(mod,'PROFILING') and mod.PROFILING:
        @wraps(func)
        def wrapped(*args,**kwargs):
            tic = time()
            out = func(*args,**kwargs)
            _timings[func].append(time() - tic)
            return out
        return wrapped
    return func

def report():
    if len(_timings) == 0:
        return ''
    else:
        results = [(f.__name__,np.mean(vals),np.std(vals)) for f, vals in _timings.iteritems()]
        longest = max(len(name) for name, _, _ in results)
        fmt = '{:>%d} {:10.3} sec avg. (std. dev. {:10.3})' % longest
        return '\n'.join(fmt.format(name,mean,std) for name, mean, std in sorted(results))

