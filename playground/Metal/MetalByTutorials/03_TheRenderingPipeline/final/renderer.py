from pyrubicon.objc.api import NSObject
#from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import ObjCProtocol
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSize

from objc_frameworks.Metal import (
  MTLCreateSystemDefaultDevice,
  MTLClearColorMake,
)

#NSObject = ObjCClass('NSObject')
MTKViewDelegate = ObjCProtocol('MTKViewDelegate')

MTKMeshBufferAllocator = ObjCClass('MTKMeshBufferAllocator')
MDLMesh = ObjCClass('MDLMesh')


#class Renderer(NSObject, auto_rename=True):
class Renderer(NSObject, protocols=[MTKViewDelegate]):

  device: 'MTLDevice' = objc_property()
  commandQueue: 'MTLCommandQueue' = objc_property()

  @objc_method
  def initWithMetalView_(self, metalView):

    if (device := MTLCreateSystemDefaultDevice()) is None and (
        commandQueue := device.newCommandQueue()) is None:
      raise ValueError('GPU not available')

    self.device = device
    self.commandQueue = commandQueue
    metalView.device = device
    
    allocator = MTKMeshBufferAllocator.alloc().initWithDevice_(device)

    send_super(__class__, self, 'init')
    metalView.clearColor = MTLClearColorMake(
      red=1,
      green=1,
      blue=0.8,
      alpha=1,
    )
    metalView.delegate = self

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

