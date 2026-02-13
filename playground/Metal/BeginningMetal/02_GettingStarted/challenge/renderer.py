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
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSize


class Renderer(NSObject):

  device: 'MTLDevice'
  commandQueue: 'MTLCommandQueue'

  @objc_method
  def initWithDevice_(self, device):
    send_super(__class__, self, 'init')
    self.device = device
    self.commandQueue = device.newCommandQueue()

    return self

  # --- MTKViewDelegate
  @objc_method
  def mtkView_drawableSizeWillChange_(self, view, size: CGSize):
    pass

  @objc_method
  def drawInMTKView_(self, view):
    if not ((drawable := view.currentDrawable) and
            (descriptor := view.currentRenderPassDescriptor)):
      return
    commandBuffer = self.commandQueue.commandBuffer()
    commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
      descriptor)
    commandEncoder.endEncoding()
    commandBuffer.presentDrawable_(drawable)
    commandBuffer.commit()

