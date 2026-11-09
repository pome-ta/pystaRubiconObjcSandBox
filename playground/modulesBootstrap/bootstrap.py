# Pythonista3 直接実行用、current directory のpath を通す

_CURRENT_DIR_NAME = 'modulesBootstrap'
_MODULES_DIR_NAME = 'pystaRubiconModules'
import sys

def hoge(file_path):
  print('hoge')
  print('file_path:')
  print(file_path)
  print('hoge_path:')
  print(__file__)
  print('')
  
  print('sys.path:')
  
  for p in sys.path:
    print('---')
    print(p)
  
  #print(sys.path)
