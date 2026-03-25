"""
Model:
let attributePosition = descriptor.attributes[0] as! MDLVertexAttribute

確認
"""

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

  sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
  sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'final'))
  #sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / 'challenge'))


from rbedge import pdbr
from objc_frameworks.Metal import MTLCreateSystemDefaultDevice
from final.nodes.model import Model

device = MTLCreateSystemDefaultDevice()

#mushroom
m = Model.alloc().initWithDevice_modelName_(device, 'mushroom')

