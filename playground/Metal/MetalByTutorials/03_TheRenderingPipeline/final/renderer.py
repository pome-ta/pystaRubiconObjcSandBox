from pathlib import Path

from pyrubicon.objc.api import NSObject
#from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import ObjCClass, ObjCProtocol
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSize

from objc_frameworks.Metal import (
  MTLCreateSystemDefaultDevice,
  MTLClearColorMake,
  MTLPrimitiveType,
)
from objc_frameworks.MetalKit import MTKMetalVertexDescriptorFromModelIO

from rbedge import pdbr

#NSObject = ObjCClass('NSObject')
MTKViewDelegate = ObjCProtocol('MTKViewDelegate')

MTKMeshBufferAllocator = ObjCClass('MTKMeshBufferAllocator')
MDLMesh = ObjCClass('MDLMesh')
SCNBox = ObjCClass('SCNBox')
MTKMesh = ObjCClass('MTKMesh')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

shader_path = Path(__file__).parent / 'Shaders.metal'


#class Renderer(NSObject, auto_rename=True):
class Renderer(NSObject, protocols=[MTKViewDelegate]):

  device: 'MTLDevice' = objc_property()
  commandQueue: 'MTLCommandQueue' = objc_property()
  library: 'MTLLibrary!' = objc_property()
  mesh: 'MTKMesh!' = objc_property()
  vertexBuffer: 'MTLBuffer!' = objc_property()
  pipelineState: 'MTLRenderPipelineState!' = objc_property()

  @objc_method
  def initWithMetalView_(self, metalView):


    if not ((device := MTLCreateSystemDefaultDevice()) and
            (commandQueue := device.newCommandQueue())):
      raise ValueError('GPU not available')

    self.device = device
    self.commandQueue = commandQueue
    metalView.device = device
    print(device)
    print(commandQueue)
    
    
    # create the mesh
    allocator = MTKMeshBufferAllocator.alloc().initWithDevice_(device)
    size = 0.8
    mdlMesh = MDLMesh.meshWithSCNGeometry_bufferAllocator_(
      SCNBox.boxWithWidth_height_length_chamferRadius_(size, size, size, 0),
      allocator)

    try:
      mesh = MTKMesh.alloc().initWithMesh(
        mdlMesh,
        device=device,
        error=None,
      )
    except Exception as e:
      print(f'{e}')

    vertexBuffer = mesh.vertexBuffers.objectAtIndexedSubscript_(0).buffer

    # create the shader function library
    source = shader_path.read_text('utf-8')
    library = device.newLibraryWithSource(
      source,
      options=MTLCompileOptions.new(),
      error=None,
    )
    self.library = library
    vertexFunction = library.newFunctionWithName_('vertex_main')
    fragmentFunction = library.newFunctionWithName_('fragment_main')

    # create the pipeline state object
    pipelineDescriptor = MTLRenderPipelineDescriptor.new()
    pipelineDescriptor.vertexFunction = vertexFunction
    pipelineDescriptor.fragmentFunction = fragmentFunction
    pipelineDescriptor.colorAttachments.objectAtIndexedSubscript_(
      0).pixelFormat = metalView.colorPixelFormat
    pipelineDescriptor.vertexDescriptor = MTKMetalVertexDescriptorFromModelIO(
      mesh.vertexDescriptor)
    try:
      pipelineState = device.newRenderPipelineStateWithDescriptor_error_(
        pipelineDescriptor, None)
    except Exception as e:
      print(f'{e}')
    
    
    send_super(__class__, self, 'init')
    metalView.clearColor = MTLClearColorMake(
      red=1,
      green=1,
      blue=0.8,
      alpha=1,
    )
    metalView.delegate = self
    #metalView.enableSetNeedsDisplay = True
    #metalView.setNeedsDisplay()

    self.mesh = mesh
    self.vertexBuffer = vertexBuffer
    self.pipelineState = pipelineState

    return self

  # --- MTKViewDelegate
  @objc_method
  def mtkView_drawableSizeWillChange_(self, view, size: CGSize):
    print('m')
    pass

  @objc_method
  def drawInMTKView_(self, view):
    print('d')
    '''
    if not ((commandBuffer := self.commandQueue.commandBuffer()) and
            (descriptor := view.currentRenderPassDescriptor) and
            (renderEncoder :=
             commandBuffer.renderCommandEncoderWithDescriptor_(descriptor))):
      return

    renderEncoder.setRenderPipelineState_(self.pipelineState)
    renderEncoder.setVertexBuffer(
      self.vertexBuffer,
      offset=0,
      atIndex=0,
    )

    for submesh in self.mesh.submeshes:
      renderEncoder.drawIndexedPrimitives(
        MTLPrimitiveType.triangle,
        indexCount=submesh.indexCount,
        indexType=submesh.indexType,
        indexBuffer=submesh.indexBuffer.buffer,
        indexBufferOffset=submesh.indexBuffer.offset,
      )

    renderEncoder.endEncoding()
    if not (drawable := view.currentDrawable):
      return
    commandBuffer.presentDrawable_(drawable)
    commandBuffer.commit()
    '''
    if not ((drawable := view.currentDrawable) and
            (descriptor := view.currentRenderPassDescriptor)):
      return

    commandBuffer = self.commandQueue.commandBuffer()
    commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
      descriptor)
    commandEncoder.endEncoding()
    commandBuffer.presentDrawable_(drawable)
    commandBuffer.commit()

