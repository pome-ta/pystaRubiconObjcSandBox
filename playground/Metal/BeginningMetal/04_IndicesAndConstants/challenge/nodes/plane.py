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
from math import sin

from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGFloat

from objc_frameworks.Metal import (
  MTLResourceOptions,
  MTLPixelFormat,
  MTLPrimitiveType,
  MTLIndexType,
)

from .node import Node


class Constants(ctypes.Structure):
  _fields_ = [
    ('animateBy', ctypes.c_float),
  ]


class Plane(Node):

  vertices: '[Float]' = objc_property(object)
  indices: '[UInt16]' = objc_property(object)
  vertexBuffer: 'MTLBuffer?' = objc_property()
  indexBuffer: 'MTLBuffer?' = objc_property()
  time: CGFloat = objc_property(CGFloat)
  constants: Constants = objc_property(object)

  @objc_method
  def initWithDevice_(self, device):
    send_super(__class__, self, 'init')
    self.vertices = (ctypes.c_float * (4 * 3))(
      -1.0,  1.0,  0.0,  # v0
      -1.0, -1.0,  0.0,  # v1
       1.0, -1.0,  0.0,  # v2
       1.0,  1.0,  0.0,  # v3
    )  # yapf: disable
    self.indices = (ctypes.c_int16 * (2 * 3))(
      0, 1, 2,
      2, 3, 0,
    )  # yapf: disable
    self.time = 0.0
    self.constants = Constants()

    self.buildBuffersDevice_(device)

    return self

  # --- private
  @objc_method
  def buildBuffersDevice_(self, device):
    vertexBuffer = device.newBufferWithBytes_length_options_(
      self.vertices, ctypes.sizeof(self.vertices),
      MTLResourceOptions.storageModeShared)
    indexBuffer = device.newBufferWithBytes_length_options_(
      self.indices, ctypes.sizeof(self.indices),
      MTLResourceOptions.storageModeShared)

    self.vertexBuffer = vertexBuffer
    self.indexBuffer = indexBuffer

  @objc_method
  def renderCommandEncoder_deltaTime_(self, commandEncoder,
                                      deltaTime: CGFloat):

    send_super(__class__,
               self,
               'renderCommandEncoder:deltaTime:',
               commandEncoder,
               deltaTime,
               argtypes=[
                 objc_id,
                 CGFloat,
               ])

    if not self.indexBuffer:
      return

    self.time += deltaTime
    animateBy = abs(sin(self.time) / 2 + 0.5)
    self.constants.animateBy = animateBy

    commandEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
    commandEncoder.setVertexBytes_length_atIndex_(
      ctypes.byref(self.constants), ctypes.sizeof(self.constants), 1)
    commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(
      MTLPrimitiveType.triangle, self.indices.__len__(), MTLIndexType.uInt16,
      self.indexBuffer, 0)


if __name__ == '__main__':
  pass

