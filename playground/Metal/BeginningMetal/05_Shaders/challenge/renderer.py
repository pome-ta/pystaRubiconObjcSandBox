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

from pyrubicon.objc.api import ObjCProtocol, NSObject
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSize

from scenes import Scene

MTKViewDelegate = ObjCProtocol('MTKViewDelegate')


class Renderer(NSObject, protocols=[
    MTKViewDelegate,
]):

  device: 'MTLDevice' = objc_property()
  commandQueue: 'MTLCommandQueue' = objc_property()

  scene: Scene = objc_property()

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

    deltaTime = 1 / view.preferredFramesPerSecond

    try:  # `scene?.`
      self.scene.renderWithCommandEncoder_deltaTime_(commandEncoder, deltaTime)
    except Exception as e:
      print(e)

    commandEncoder.endEncoding()
    commandBuffer.presentDrawable_(drawable)
    commandBuffer.commit()


if __name__ == '__main__':
  from objc_frameworks.Metal import MTLCreateSystemDefaultDevice
  from rbedge import pdbr

  renderer = Renderer.alloc().initWithDevice_(MTLCreateSystemDefaultDevice())

