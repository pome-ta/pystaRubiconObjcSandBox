import ctypes
from pathlib import Path

from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super

from objc_frameworks.Metal import MTLResourceOptions, MTLPixelFormat

from .node import Node
from .model import Model
from .renderable import Renderable

from simdTypes import ModelConstants

MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

ROOT_PATH = Path(__file__).parents[1]

shader_path = ROOT_PATH / 'Shader.metal'


class Instance(Node, protocols=[
    Renderable,
]):

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
  def initWithDevice_modelName_instances_(self, device, modelName: object,
                                          instances: int):

    self.model = Model.alloc().initWithDevice_modelName_(device, modelName)
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
      len(self.instanceConstants) * ctypes.sizeof(ModelConstants),
      MTLResourceOptions.storageModeShared)

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
        pipelineDescriptor, None)
    except Exception as e:
      print(f'pipelineState error: {e}')

    return pipelineState

