import os, runpy, sys
here = os.path.dirname(os.path.abspath(__file__))
for mod in ('bn1_chipcodes', 'bn1_arealabels'):
    d = os.path.join(here, '..', mod)
    sys.path.insert(0, d)
    runpy.run_path(os.path.join(d, 'prebuild.py'), run_name='__main__')
    sys.path.remove(d)
