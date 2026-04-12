import ctypes
from pathlib import Path

from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super

from objc_frameworks.Metal import (
  MTLResourceOptions,
  MTLPixelFormat,
)

from rbedge.simd import matrix_multiply
from rbedge import pdbr

from .node import Node
from .model import Model
from .renderable import Renderable

from simdTypes import ModelConstants

MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

ROOT_PATH = Path(__file__).parents[1]

shader_path = ROOT_PATH / 'Shader.metal'


class Instance(
    Node,
    protocols=[
      Renderable,
    ],
):

  model: Model = objc_property()

  nodes: '[Node]()' = objc_property(object)
  instanceConstants: '[ModelConstants]()' = objc_property(object)

  modelConstants: ModelConstants = objc_property(object)

  instanceBuffer: 'MTLBuffer?' = objc_property()

  # Renderable
  pipelineState: 'MTLRenderPipelineState!' = objc_property()
  vertexFunctionName: str = objc_property(object)

  fragmentFunctionName: str = objc_property(object)
  vertexDescriptor: 'MTLVertexDescriptor' = objc_property()

  @objc_method
  def initializeProperties(self):
    # todo: class member declarations
    send_super(__class__, self, 'initializeProperties')

    self.nodes = []
    self.instanceConstants = []

    self.modelConstants = ModelConstants()

    # Renderable
    self.vertexFunctionName = 'vertex_instance_shader'

  @objc_method
  def initWithDevice_modelName_instances_(
    self,
    device,
    modelName: object,
    instances: int,
  ):

    self.model = Model.alloc().initWithDevice_modelName_(
      device,
      modelName,
    )
    self.vertexDescriptor = self.model.vertexDescriptor
    self.fragmentFunctionName = self.model.fragmentFunctionName

    send_super(__class__, self, 'init')
    self.initializeProperties()

    self.name = modelName
    self.createInstances_(instances)
    self.makeBufferWithDevice_(device)

    self.pipelineState = self.buildPipelineStateWithDevice_(device)

    return self

  @objc_method
  def createInstances_(self, instances: int):
    for i in range(instances):
      node = Node.new()
      node.name = f'Instance {i}'
      self.nodes.append(node)
      self.instanceConstants.append(ModelConstants())

  @objc_method
  def makeBufferWithDevice_(self, device):
    self.instanceBuffer = device.newBufferWithLength_options_(
      len(self.instanceConstants) * ModelConstants.stride,
      MTLResourceOptions.storageModeShared,
    )

    self.instanceBuffer.label = 'Instance Buffer'

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

    if not ((instanceBuffer := self.instanceBuffer) and len(self.nodes) > 0):
      return

    #base_address = ctypes.cast(instanceBuffer.contents, ctypes.c_void_p).value
    pointer = ctypes.cast(instanceBuffer.contents, ctypes.c_void_p).value
    #constants = ModelConstants()
    pointee = ModelConstants()

    for idx, node in enumerate(self.nodes):
      #mv_matrix = matrix_multiply(modelViewMatrix, node.modelMatrix)
      pointee.modelViewMatrix = matrix_multiply(modelViewMatrix,
                                                node.modelMatrix)
      pointee.materialColor = node.materialColor
      #constants.normalMatrix = mv_matrix.upperLeft3x3()
      #constants.shininess = node.shininess
      #constants.specularIntensity = node.specularIntensity

      dst_address = pointer + (idx * ModelConstants.size)
      ctypes.memmove(
        dst_address,
        ctypes.addressof(pointee.raw),
        ModelConstants.size,
      )
    '''
    pointer = ctypes.cast(
      instanceBuffer.contents,
      ctypes.POINTER(ModelConstants),
    )

    for idx, node in enumerate(self.nodes):
      pointer[idx].modelViewMatrix = matrix_multiply(
        modelViewMatrix,
        node.modelMatrix,
      )
      pointer[idx].materialColor = node.materialColor
    

    '''

    commandEncoder.setFragmentTexture_atIndex_(self.model.texture, 0)
    commandEncoder.setRenderPipelineState_(self.pipelineState)
    commandEncoder.setVertexBuffer_offset_atIndex_(instanceBuffer, 0, 1)

    if not ((meshes := self.model.meshes) and len(meshes) > 0):
      return

    for mesh in meshes:
      vertexBuffer = mesh.vertexBuffers.objectAtIndexedSubscript_(0)
      commandEncoder.setVertexBuffer_offset_atIndex_(
        vertexBuffer.buffer,
        vertexBuffer.offset,
        0,
      )

      for submesh in mesh.submeshes:
        commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_instanceCount_(
          submesh.primitiveType,
          submesh.indexCount,
          submesh.indexType,
          submesh.indexBuffer.buffer,
          submesh.indexBuffer.offset,
          len(self.nodes),
        )

