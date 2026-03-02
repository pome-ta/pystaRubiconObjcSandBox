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


from pyrubicon.objc.api import objc_const, ObjCInstance
from pyrubicon.objc.runtime import load_library

#MetalKit = load_library('MetalKit')
framework = load_library('MetalKit')

def get_const(global_variable_name) -> ObjCInstance:
  return objc_const(framework, global_variable_name)


MTKTextureLoaderOriginBottomLeft = get_const('MTKTextureLoaderOriginBottomLeft')

print(str(MTKTextureLoaderOriginBottomLeft))


if __name__ == '__main__':
  pass
