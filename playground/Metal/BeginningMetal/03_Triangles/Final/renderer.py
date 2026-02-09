_TOP_DIR_NAME = 'pystaRubiconObjcSandBox'
_MODULES_DIR_NAME = 'modules'

# todo: `./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME}` にあるpackage のimport 準備
if __name__ == '__main__' and not __file__[:__file__.rfind('/')].endswith(
    _TOP_DIR_NAME):
  import pathlib
  import sys
  __parents = pathlib.Path(__file__).resolve().parents
  for path in __parents:
    if path.name == _TOP_DIR_NAME and (__modules_path :=
                                       path / _MODULES_DIR_NAME).exists():
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

from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSize

err_ptr = ctypes.c_void_p()

shader_path = Path('./Shader.metal')
#source = shader_path.read_text('utf-8')


class Renderer(NSObject):

  device: 'MTLDevice' = objc_property()
  commandQueue: 'MTLCommandQueue' = objc_property()
  vertices: '[Float]' = (ctypes.c_float * 9)(
     0.0,  1.0,  0.0,  # 1
    -1.0, -1.0,  0.0,  # 2
     1.0, -1.0,  0.0,  # 3
  )  # yapf: disable

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

