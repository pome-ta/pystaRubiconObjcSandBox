import ctypes
from pathlib import Path

from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import NSDictionary
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGFloat

from objc_frameworks.Metal import (
  MTLVertexFormat,
  MTLPixelFormat,
)

from objc_frameworks.MetalKit import (
  MTKTextureLoaderOptionOrigin,
  MTKTextureLoaderOriginBottomLeft,
)

from objc_frameworks.MetalKit import MTKModelIOVertexDescriptorFromMetal

from objc_frameworks.ModelIO import (
  MDLVertexAttributePosition,
  MDLVertexAttributeColor,
  MDLVertexAttributeTextureCoordinate,
  MDLVertexAttributeNormal,
)

from objc_frameworks.SceneKit import SCNVector3


from rbedge.utils import nsurl, get_str_filepath
from rbedge.utils import readonly_properties
from rbedge.simd import (
  simd_float2,
  simd_float3,
  simd_float4,
  matrix_multiply,
)
from rbedge import pdbr

from .node import Node
from .renderable import Renderable
from .texturable import Texturable

from simdTypes import (
  Vertex,
  ModelConstants,
)

MDLVertexAttribute = ObjCClass('MDLVertexAttribute')
MTKMeshBufferAllocator = ObjCClass('MTKMeshBufferAllocator')
MDLAsset = ObjCClass('MDLAsset')
MTKMesh = ObjCClass('MTKMesh')

MTLVertexDescriptor = ObjCClass('MTLVertexDescriptor')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

MTKTextureLoader = ObjCClass('MTKTextureLoader')

SCNScene = ObjCClass('SCNScene')


ROOT_PATH = Path(__file__).parents[1]


# wip: 雑
def _get_filepath(file_name: str) -> str | None:
  root = ROOT_PATH.parents[1] / 'assets'
  return get_str_filepath(root, file_name)


def get_image_path(imageName: str) -> str | None:
  return _get_filepath(imageName)


def get_model_path(
  modelName: str,
  extension: str = '',
) -> str | None:
  return _get_filepath(f'{modelName}.{extension}')


shader_path = ROOT_PATH / 'Shader.metal'


@readonly_properties('vertexDescriptor')
class Model(
    Node,
    protocols=[
      Renderable,
      Texturable,
    ],
):

  meshes: '[AnyObject]?' = objc_property()

  # Texturable
  texture: 'MTLTexture?' = objc_property()

  # Renderable
  pipelineState: 'MTLRenderPipelineState!' = objc_property()
  vertexFunctionName: str = objc_property(object)
  fragmentFunctionName: str = objc_property(object)
  modelConstants: ModelConstants = objc_property(object)

  @objc_method  # declare_property - getter
  def vertexDescriptor(self) -> ObjCInstance:
    vertexDescriptor = MTLVertexDescriptor.new()
    # todo: `objectAtIndexedSubscript_` 長いので配列処理
    range_num: int = 4
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
          attribute.offset = ctypes.sizeof(ctypes.c_float) * 3
          attribute.bufferIndex = 0
        case 2:
          attribute.format = MTLVertexFormat.float2
          attribute.offset = ctypes.sizeof(ctypes.c_float) * 7
          attribute.bufferIndex = 0
        case 3:
          attribute.format = MTLVertexFormat.float3
          attribute.offset = ctypes.sizeof(ctypes.c_float) * 9
          attribute.bufferIndex = 0
        case _:
          import logging
          error = IndexError(f'{idx=}: list index out of range')
          logging.warning(f'{type(error).__name__} -> {error}')

    vertexDescriptor.layouts.objectAtIndexedSubscript_(
      0).stride = ctypes.sizeof(ctypes.c_float) * 12

    return vertexDescriptor

  @objc_method
  def initializeProperties(self):
    # todo: class member declarations
    send_super(__class__, self, 'initializeProperties')

    # Renderable
    self.fragmentFunctionName = 'fragment_color'
    self.vertexFunctionName = 'vertex_shader'
    self.modelConstants = ModelConstants()

  @objc_method
  def initWithDevice_modelName_(self, device, modelName: object):
    send_super(__class__, self, 'init')
    self.initializeProperties()

    self.name = modelName
    self.loadModelWithDevice_modelName_(device, modelName)

    imageName = modelName + '.png'

    if (texture := self.setTextureWithDevice_imageName_(device, imageName)):
      self.texture = texture
      self.fragmentFunctionName = 'lit_textured_fragment'

    self.pipelineState = self.buildPipelineStateWithDevice_(device)

    return self

  @objc_method
  def loadModelWithDevice_modelName_(self, device, modelName: object):
    if not (assetURL := get_model_path(modelName, 'obj')):
      raise ValueError(f'Asset {modelName} does not exist.')

    descriptor = MTKModelIOVertexDescriptorFromMetal(self.vertexDescriptor)

    range_num: int = 4
    for idx, attribute in enumerate([
        descriptor.attributes.objectAtIndexedSubscript_(i)
        for i in range(range_num)
    ]):
      match idx:
        case 0:
          if not isinstance(
            (attributePosition := attribute), MDLVertexAttribute):
            raise ValueError(f'{idx}: {attribute=}')
          attributePosition.name = MDLVertexAttributePosition
          descriptor.attributes.setObject_atIndexedSubscript_(
            attributePosition,
            idx,
          )
        case 1:
          if not isinstance((attributeColor := attribute), MDLVertexAttribute):
            raise ValueError(f'{idx}: {attribute=}')
          attributeColor.name = MDLVertexAttributeColor
          descriptor.attributes.setObject_atIndexedSubscript_(
            attributeColor,
            idx,
          )
        case 2:
          if not isinstance(
            (attributeTexture := attribute), MDLVertexAttribute):
            raise ValueError(f'{idx}: {attribute=}')
          attributeTexture.name = MDLVertexAttributeTextureCoordinate
          descriptor.attributes.setObject_atIndexedSubscript_(
            attributeTexture,
            idx,
          )
        case 3:
          if not isinstance(
            (attributeNormal := attribute), MDLVertexAttribute):
            raise ValueError(f'{idx}: {attribute=}')
          attributeNormal.name = MDLVertexAttributeNormal
          descriptor.attributes.setObject_atIndexedSubscript_(
            attributeNormal,
            idx,
          )
        case _:
          import logging
          error = IndexError(f'{idx=}: list index out of range')
          logging.warning(f'{type(error).__name__} -> {error}')

    bufferAllocator = MTKMeshBufferAllocator.alloc().initWithDevice_(device)

    asset = MDLAsset.alloc().initWithURL_vertexDescriptor_bufferAllocator_(
      nsurl(assetURL),
      descriptor,
      bufferAllocator,
    )

    scnScene = SCNScene.sceneWithMDLAsset_(asset)
    boundingBox = scnScene.rootNode.getBoundingBox()
    #print('---')
    pdbr.state(boundingBox)
    #print(f'maxBounds: {boundingBox.max}')
    #print(f'minBounds: {boundingBox.min}')
    #pdbr.state(scnScene.rootNode.childNodes.firstObject().getBoundingBox())
    #pdbr.state(scnScene.rootNode.getBoundingBox())
    '''
    
    boundingBox = send_message(
      asset,
      'boundingBox',
      restype=MDLAxisAlignedBoundingBox,
      argtypes=[],
    )
    '''

    #pdbr.state(asset)

    #pdbr.state(asset)
    #print(f'maxBounds: {boundingBox.maxBounds}')
    #print(f'minBounds: {boundingBox.minBounds}')
    #print(boundingBox.minBounds)
    #print(asset.boundingBox.maxBounds.x)
    #boundingBox = asset.boundingBox
    #self.width = boundingBox.maxBounds.x - boundingBox.minBounds.x
    #self.height = boundingBox.maxBounds.y - boundingBox.minBounds.y

    try:
      self.meshes = MTKMesh.newMeshesFromAsset_device_sourceMeshes_error_(
        asset,
        device,
        None,
        None,
      )
    except Exception as e:
      print(e)

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
      origin,
      MTKTextureLoaderOptionOrigin,
    )

    if (textureURL := get_image_path(imageName)):
      try:
        texture = textureLoader.newTextureWithContentsOfURL_options_error_(
          nsurl(textureURL),
          textureLoaderOptions,
          None,
        )

      except Exception:
        print('texture not created')

    return texture

  # --- Renderable
  # --- extension Renderable
  @objc_method
  def buildPipelineStateWithDevice_(self, device) -> ObjCInstance:
    source = shader_path.read_text('utf-8')
    options = MTLCompileOptions.new()

    library = device.newLibraryWithSource_options_error_(
      source,
      options,
      None,
    )

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
        pipelineDescriptor,
        None,
      )
    except Exception as e:
      print(f'pipelineState error: {e}')

    return pipelineState

  # --- extension Renderable
  @objc_method
  def doRenderWithCommandEncoder_modelViewMatrix_(
    self,
    commandEncoder,
    modelViewMatrix: object,
  ):
    self.modelConstants.modelViewMatrix = modelViewMatrix
    self.modelConstants.materialColor = self.materialColor
    self.modelConstants.normalMatrix = modelViewMatrix.upperLeft3x3()
    self.modelConstants.shininess = self.shininess
    self.modelConstants.specularIntensity = self.specularIntensity

    commandEncoder.setVertexBytes_length_atIndex_(
      self.modelConstants.raw,
      self.modelConstants.stride,
      1,
    )
    if self.texture != None:
      commandEncoder.setFragmentTexture_atIndex_(self.texture, 0)
    commandEncoder.setRenderPipelineState_(self.pipelineState)

    if not ((meshes := self.meshes) and len(self.meshes) > 0):
      return

    for mesh in meshes:
      vertexBuffer = mesh.vertexBuffers.objectAtIndexedSubscript_(0)
      commandEncoder.setVertexBuffer_offset_atIndex_(
        vertexBuffer.buffer,
        vertexBuffer.offset,
        0,
      )
      for submesh in mesh.submeshes:
        commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(
          submesh.primitiveType,
          submesh.indexCount,
          submesh.indexType,
          submesh.indexBuffer.buffer,
          submesh.indexBuffer.offset,
        )

