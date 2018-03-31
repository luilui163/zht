# Used successfully in Python2.5 with matplotlib 0.91.2 and PyQt4 (and Qt 4.3.3)
from distutils.core import setup
import py2exe
setup(windows=[{"script":"GUI_v3_27.py"}],
     options={"py2exe":{"packages":['matplotlib'],
                        'dll_excludes':['api-ms-win-core-processthreads-l1-1-2.dll']
                        }})