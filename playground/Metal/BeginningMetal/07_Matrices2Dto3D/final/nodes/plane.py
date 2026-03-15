import ctypes
from pathlib import Path
from math import sin, radians

from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import NSDictionary
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
from objc_frameworks.MetalKit import (
  MTKTextureLoaderOptionOrigin,
  MTKTextureLoaderOriginBottomLeft,
)

from rbedge.simd import matrix_multiply
from rbedge.utils import nsurl
from rbedge import pdbr

from .node import Node
from .renderable import Renderable
from .texturable import Texturable
from simdTypes import (
  Vertex,
  simd_float2,
  simd_float3,
  simd_float4,
  ModelConstants,
)

from matrixMath import matrix_float4x4

MTLVertexDescriptor = ObjCClass('MTLVertexDescriptor')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

MTKTextureLoader = ObjCClass('MTKTextureLoader')

ROOT_PATH = Path(__file__).parents[1]


# wip: 雑
def get_image_path(imageName: str) -> str:
  root = ROOT_PATH / 'Images'
  for file in root.iterdir():
    if file.name == imageName:
      return str(file.resolve())


shader_path = ROOT_PATH / 'Shader.metal'


class Plane(Node, protocols=[
    Renderable,
    Texturable,
]):

  vertices: '[Vertices]' = objc_property(object)
  indices: '[UInt16]' = objc_property(object)
  vertexBuffer: 'MTLBuffer?' = objc_property()
  indexBuffer: 'MTLBuffer?' = objc_property()
  time: CGFloat = objc_property(CGFloat)
  modelConstants: ModelConstants = objc_property(object)
  # Renderable
  pipelineState: 'MTLRenderPipelineState!' = objc_property()
  vertexFunctionName: str = objc_property(object)
  fragmentFunctionName: str = objc_property(object)
  vertexDescriptor: 'MTLVertexDescriptor' = objc_property()
  # Texturable
  texture: 'MTLTexture?' = objc_property()
  maskTexture: 'MTLTexture?' = objc_property()

  @objc_method
  def initializeProperties(self):
    # todo: class member declarations
    send_super(__class__, self, 'initializeProperties')

    self.vertices = (Vertex * 4)(
      Vertex(  # v0
        position=simd_float3(-1.0,  1.0,  0.0), color=simd_float4(1.0, 0.0, 0.0, 1.0), texture=simd_float2(0.0, 1.0)),
      Vertex(  # v1
        position=simd_float3(-1.0, -1.0,  0.0), color=simd_float4(0.0, 1.0, 0.0, 1.0), texture=simd_float2(0.0, 0.0)),
      Vertex(  # v2
        position=simd_float3( 1.0, -1.0,  0.0), color=simd_float4(0.0, 0.0, 1.0, 1.0), texture=simd_float2(1.0, 0.0)),
      Vertex(  # v3
        position=simd_float3( 1.0,  1.0,  0.0), color=simd_float4(1.0, 0.0, 1.0, 1.0), texture=simd_float2(1.0, 1.0)),
    )  # yapf: disable

    self.indices = (ctypes.c_uint16 * (2 * 3))(
      0, 1, 2,
      2, 3, 0,
    )  # yapf: disable

    self.time = 0.0
    self.modelConstants = ModelConstants(matrix_float4x4.identity())

    # Renderable
    self.fragmentFunctionName = 'fragment_shader'
    self.vertexFunctionName = 'vertex_shader'

    vertexDescriptor = MTLVertexDescriptor.new()
    # todo: `objectAtIndexedSubscript_` 長いので配列処理
    range_num = 3
    for idx, attribute in enumerate([
        vertexDescriptor.attributes.objectAtIndexedSubscript_(i)
        for i in range(range_num)
    ]):
      match idx:
        case 0:
          attribute.format = MTLVertexFormat.float3
          attribute.offset = 0
          attribute.bufferIndex = 0
        case 1:
          attribute.format = MTLVertexFormat.float4
          attribute.offset = simd_float3.stride
          attribute.bufferIndex = 0
        case 2:
          attribute.format = MTLVertexFormat.float2
          attribute.offset = simd_float3.stride + simd_float4.stride
          attribute.bufferIndex = 0
        case _:
          import logging
          error = IndexError(f'{idx=}: list index out of range')
          logging.warning(f'{type(error).__name__} -> {error}')

    vertexDescriptor.layouts.objectAtIndexedSubscript_(
      0).stride = ctypes.sizeof(Vertex)
    self.vertexDescriptor = vertexDescriptor

  @objc_method
  def initWithDevice_(self, device):
    send_super(__class__, self, 'init')
    self.initializeProperties()

    self.buildBuffersWithDevice_(device)
    self.pipelineState = self.buildPipelineStateWithDevice_(device)

    return self

  @objc_method
  def initWithDevice_imageName_(self, device, imageName: object):
    send_super(__class__, self, 'init')
    self.initializeProperties()

    if (texture := self.setTextureWithDevice_imageName_(device, imageName)):
      self.texture = texture
      self.fragmentFunctionName = 'textured_fragment'

    self.buildBuffersWithDevice_(device)
    self.pipelineState = self.buildPipelineStateWithDevice_(device)

    return self

  @objc_method
  def initWithDevice_imageName_maskImageName_(self, device, imageName: object,
                                              maskImageName: object):
    send_super(__class__, self, 'init')
    self.initializeProperties()

    if (texture := self.setTextureWithDevice_imageName_(device, imageName)):
      self.texture = texture
      self.fragmentFunctionName = 'textured_fragment'

    if (maskTexture :=
        self.setTextureWithDevice_imageName_(device, maskImageName)):
      self.maskTexture = maskTexture
      self.fragmentFunctionName = 'textured_mask_fragment'

    self.buildBuffersWithDevice_(device)
    self.pipelineState = self.buildPipelineStateWithDevice_(device)

    return self

  # --- Texturable
  # --- extension Texturable
  @objc_method
  def setTextureWithDevice_imageName_(self, device,
                                      imageName: object) -> ObjCInstance:
    texture = None
    textureLoader = MTKTextureLoader.alloc().initWithDevice_(device)
    # todo: `#available(iOS 10.0, *)` 古すぎるので処理しない
    origin = str(MTKTextureLoaderOriginBottomLeft)

    textureLoaderOptions = NSDictionary.dictionaryWithObject_forKey_(
      origin, MTKTextureLoaderOptionOrigin)

    if (textureURL := nsurl(get_image_path(imageName))):
      try:
        texture = textureLoader.newTextureWithContentsOfURL_options_error_(
          textureURL, textureLoaderOptions, None)

      except Exception:
        print('texture not created')

    return texture

  # --- Renderable
  # --- extension Renderable
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
      pipelineState = device.newRenderPipelineStateWithDescriptor_error_(
        pipelineDescriptor, None)
    except Exception as e:
      print(f'pipelineState error: {e}')

    return pipelineState

  # --- private
  @objc_method
  def buildBuffersWithDevice_(self, device):
    vertexBuffer = device.newBufferWithBytes_length_options_(
      self.vertices, ctypes.sizeof(self.vertices),
      MTLResourceOptions.storageModeShared)
    indexBuffer = device.newBufferWithBytes_length_options_(
      self.indices, ctypes.sizeof(self.indices),
      MTLResourceOptions.storageModeShared)

    self.vertexBuffer = vertexBuffer
    self.indexBuffer = indexBuffer

  @objc_method
  def renderWithCommandEncoder_deltaTime_(self, commandEncoder,
                                          deltaTime: CGFloat):
    send_super(__class__,
               self,
               'renderWithCommandEncoder:deltaTime:',
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

    rotationMatrix = matrix_float4x4.rotationAngle(animateBy, 0.0, 0.0, 1.0)
    viewMatrix = matrix_float4x4.translation(0.0, 0.0, -4.0)
    modelViewMatrix = matrix_multiply(rotationMatrix, viewMatrix)
    self.modelConstants.modelViewMatrix = modelViewMatrix

    aspect = 750.0 / 1334.0
    projectionMatrix = matrix_float4x4.projectionFov(radians(65), aspect, 0.1,
                                                     100.0)
    self.modelConstants.modelViewMatrix = matrix_multiply(
      projectionMatrix, modelViewMatrix)

    commandEncoder.setRenderPipelineState_(self.pipelineState)
    commandEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)

    commandEncoder.setVertexBytes_length_atIndex_(
      ctypes.byref(self.modelConstants), ctypes.sizeof(self.modelConstants), 1)
    commandEncoder.setFragmentTexture_atIndex_(self.texture, 0)
    commandEncoder.setFragmentTexture_atIndex_(self.maskTexture, 1)
    commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(
      MTLPrimitiveType.triangle, self.indices.__len__(), MTLIndexType.uInt16,
      self.indexBuffer, 0)

