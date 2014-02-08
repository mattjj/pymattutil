from __future__ import division
import numpy as np
import line_profiler, sys, StringIO, inspect, os, functools, time, collections

# use @line_profiled for a thin wrapper around line_profiler

_prof = line_profiler.LineProfiler()

def line_profiled(func):
    mod = inspect.getmodule(func)
    if 'PROFILING' in os.environ or (hasattr(mod,'PROFILING') and mod.PROFILING):
        return _prof(func)
    return func

def show_line_stats(stream=None):
    _prof.print_stats(stream=stream)

# use @timed for really basic timing

_timings = collections.defaultdict(list)

def timed(func):
    @functools.wraps(func)
    def wrapped(*args,**kwargs):
        tic = time.time()
        out = func(*args,**kwargs)
        _timings[func].append(time.time() - tic)
        return out
    return wrapped

def show_timings(stream=None):
    if stream is None:
        stream = sys.stdout
    if len(_timings) > 0:
        results = [(inspect.getsourcefile(f),f.__name__,np.mean(vals),np.std(vals))
                for f, vals in _timings.iteritems()]
        filename_lens = max(len(filename) for filename, _, _, _ in results)
        name_lens = max(len(name) for _, name, _, _ in results)
        fmt = '{:>%d} {:>%d} {:10.3} sec avg. (std. dev. {:10.3})' % (filename_lens, name_lens)
        print >>stream, '\n'.join(fmt.format(filename,name,mean,std)
                for filename, name, mean, std in sorted(results))

