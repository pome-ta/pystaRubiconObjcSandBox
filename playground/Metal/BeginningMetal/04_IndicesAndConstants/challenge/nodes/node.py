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

from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGFloat

from rbedge import pdbr


class Node(NSObject):
  name: str = objc_property(object)
  #children: ['Node'] = objc_property(object, weak=True)
  children: ['Node'] = objc_property(object)

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')

    self.name = 'Untitled'
    self.children = []

    return self

  @objc_method
  def addChildNode_(self, childNode):
    self.children.append(childNode)

  @objc_method
  def renderCommandEncoder_deltaTime_(self, commandEncoder,
                                      deltaTime: CGFloat):

    [
      child.renderCommandEncoder_deltaTime_(commandEncoder, deltaTime)
      for child in self.children
    ]


if __name__ == '__main__':
  pass

