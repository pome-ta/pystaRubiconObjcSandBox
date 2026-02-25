import ctypes
from math import sin

from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGFloat

from objc_frameworks.Metal import (
  MTLResourceOptions,
  MTLPrimitiveType,
  MTLIndexType,
)

from .node import Node
from simdTypes import Vertex


class Vertices(ctypes.Structure):
  _fields_ = [
    ('vertex', Vertex * 4),
  ]


class Constants(ctypes.Structure):
  _fields_ = [
    ('animateBy', ctypes.c_float),
  ]


class Plane(Node):

  vertices: '[Vertices]' = objc_property(object)
  indices: '[UInt16]' = objc_property(object)
  vertexBuffer: 'MTLBuffer?' = objc_property()
  indexBuffer: 'MTLBuffer?' = objc_property()
  time: CGFloat = objc_property(CGFloat)
  constants: Constants = objc_property(object)

  @objc_method
  def initWithDevice_(self, device):
    send_super(__class__, self, 'init')

    self.vertices = Vertices((
      Vertex(  # v0
        position=(-1.0,  1.0,  0.0), color=(1.0, 0.0, 0.0, 1.0)),
      Vertex(  # v1
        position=(-1.0, -1.0,  0.0), color=(0.0, 1.0, 0.0, 1.0)),
      Vertex(  # v2
        position=( 1.0, -1.0,  0.0), color=(0.0, 0.0, 1.0, 1.0)),
      Vertex(  # v3
        position=( 1.0,  1.0,  0.0), color=(1.0, 0.0, 1.0, 1.0)),
    ))  # yapf: disable

    '''
    self.vertices = (ctypes.c_float * (4 * 3))(
      -1.0,  1.0,  0.0,  # v0
      -1.0, -1.0,  0.0,  # v1
       1.0, -1.0,  0.0,  # v2
       1.0,  1.0,  0.0,  # v3
    )  # yapf: disable
    '''

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
      self.vertices,
      ctypes.sizeof(self.vertices),
      MTLResourceOptions.storageModeShared)
    indexBuffer = device.newBufferWithBytes_length_options_(
      self.indices,
      self.indices.__len__() * ctypes.sizeof(self.indices),
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

