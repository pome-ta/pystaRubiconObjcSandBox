_TOP_DIR_NAME = 'pystaRubiconObjcSandBox'
_MODULES_DIR_NAME = 'modules'

# todo: `./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME}` にあるpackage のimport 準備
if __name__ == '__main__' and not __file__[:__file__.rfind('/')].endswith(
    _TOP_DIR_NAME):
  import pathlib
  import sys
  __parents = pathlib.Path(__file__).resolve().parents
  for __dir_path in __parents:
    if __dir_path.name == _TOP_DIR_NAME and (__modules_path := __dir_path /
                                             _MODULES_DIR_NAME).exists():
      sys.path.insert(0, str(__modules_path))
      break
  else:
    import warnings
    with warnings.catch_warnings():
      warnings.simplefilter('always', ImportWarning)
      __warning_message = f'./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME} not found in parent directories'
      warnings.warn(__warning_message, ImportWarning)

import ctypes
from pathlib import Path

from pyrubicon.objc.api import ObjCClass, ObjCProtocol, NSObject

MTKViewDelegate = ObjCProtocol('MTKViewDelegate')

ROOT_PATH = Path(__file__).parents[0]
shader_path = ROOT_PATH / 'Shaders.metal'

#class Renderer(NSObject, auto_rename=True):
class Renderer(NSObject):
  pass

if __name__ == '__main__':
  #print(shader_path.exists())
  #Renderer.auto_rename = True
  pass
