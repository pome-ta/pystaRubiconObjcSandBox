import ctypes
from pathlib import Path
from math import sin

from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGFloat

from objc_frameworks.Metal import (
  MTLResourceOptions,
  MTLPrimitiveType,
  MTLIndexType,
  MTLVertexFormat,
  MTLPixelFormat,
)

MTLVertexDescriptor = ObjCClass('MTLVertexDescriptor')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

from .node import Node
from .renderable import Renderable
from simdTypes import Vertex, Position


class Vertices(ctypes.Structure):
  _fields_ = [
    ('vertex', Vertex * 4),
  ]


class Constants(ctypes.Structure):
  _fields_ = [
    ('animateBy', ctypes.c_float),
  ]


shader_path = Path(__file__).parents[1] / 'Shader.metal'


class Plane(Node, protocols=[
    Renderable,
]):

  vertices: '[Vertices]' = objc_property(object)
  indices: '[UInt16]' = objc_property(object)
  vertexBuffer: 'MTLBuffer?' = objc_property()
  indexBuffer: 'MTLBuffer?' = objc_property()
  time: CGFloat = objc_property(CGFloat)
  constants: Constants = objc_property(object)
  # Renderable
  pipelineState: 'MTLRenderPipelineState!' = objc_property()
  vertexFunctionName: str = objc_property(object)
  fragmentFunctionName: str = objc_property(object)
  vertexDescriptor: 'MTLVertexDescriptor' = objc_property()

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

    self.indices = (ctypes.c_int16 * (2 * 3))(
      0, 1, 2,
      2, 3, 0,
    )  # yapf: disable

    self.time = 0.0
    self.constants = Constants()

    # Renderable
    print('plane')
    self.fragmentFunctionName = 'fragment_shader'
    self.vertexFunctionName = 'vertex_shader'

    vertexDescriptor = MTLVertexDescriptor.new()
    # todo: `objectAtIndexedSubscript_` 長いので配列処理
    for idx, attribute in enumerate([
        vertexDescriptor.attributes.objectAtIndexedSubscript_(i)
        for i in range(2)
    ]):
      match idx:
        case 0:
          attribute.format = MTLVertexFormat.float3
          attribute.offset = 0
          attribute.bufferIndex = 0
        case 1:
          attribute.format = MTLVertexFormat.float4
          attribute.offset = ctypes.sizeof(Position)
          attribute.bufferIndex = 0
        case _:
          import logging
          error = IndexError(f'{idx=}: list index out of range')
          logging.warning(f'{type(error).__name__} -> {error}')

    vertexDescriptor.layouts.objectAtIndexedSubscript_(
      0).stride = ctypes.sizeof(Vertex)
    self.vertexDescriptor = vertexDescriptor

    self.buildBuffersDevice_(device)
    #self.pipelineState = self.buildPipelineStateWithDevice_(device)

    return self

  # --- Renderable
  @objc_method
  def buildPipelineStateWithDevice_(self, device) -> ObjCInstance:
    source = shader_path.read_text('utf-8')
    options = MTLCompileOptions.new()

    library = device.newLibraryWithSource_options_error_(source, options, None)

    vertexFunction = library.newFunctionWithName_(self.vertexFunctionName)
    fragmentFunction = library.newFunctionWithName_(self.fragmentFunctionName)

    pipelineDescriptor = MTLRenderPipelineDescriptor.new()
    pipelineDescriptor.vertexFunction = vertexFunction
    pipelineDescriptor.fragmentFunction = fragmentFunction
    pipelineDescriptor.colorAttachments.objectAtIndexedSubscript_(
      0).pixelFormat = MTLPixelFormat.bgra8Unorm

    pipelineDescriptor.vertexDescriptor = self.vertexDescriptor

    pipelineState = None
    try:
      pipelineState = self.device.newRenderPipelineStateWithDescriptor_error_(
        pipelineDescriptor, None)
    except Exception as e:
      print(f'pipelineState error: {e}')

    return pipelineState

  # --- private
  @objc_method
  def buildBuffersDevice_(self, device):
    vertexBuffer = device.newBufferWithBytes_length_options_(
      ctypes.byref(self.vertices), ctypes.sizeof(self.vertices),
      MTLResourceOptions.storageModeShared)
    indexBuffer = device.newBufferWithBytes_length_options_(
      self.indices,
      self.indices.__len__() * ctypes.sizeof(self.indices),
      MTLResourceOptions.storageModeShared)

    self.vertexBuffer = vertexBuffer
    self.indexBuffer = indexBuffer

  @objc_method
  def renderWithCommandEncoder_deltaTime_(self, commandEncoder,
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

    commandEncoder.setRenderPipelineState_(self.pipelineState)

    commandEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
    commandEncoder.setVertexBytes_length_atIndex_(
      ctypes.byref(self.constants), ctypes.sizeof(self.constants), 1)
    commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(
      MTLPrimitiveType.triangle, self.indices.__len__(), MTLIndexType.uInt16,
      self.indexBuffer, 0)

