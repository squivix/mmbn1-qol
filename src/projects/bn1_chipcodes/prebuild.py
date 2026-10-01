import runpy, os
runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_glyphs.py'), run_name='__main__')
