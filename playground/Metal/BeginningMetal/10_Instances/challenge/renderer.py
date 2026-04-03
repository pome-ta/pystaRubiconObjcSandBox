from pyrubicon.objc.api import ObjCClass, ObjCProtocol, NSObject
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSize

from objc_frameworks.Metal import (
  MTLSamplerMinMagFilter,
  MTLCompareFunction,
)

from scenes import Scene

MTLSamplerDescriptor = ObjCClass('MTLSamplerDescriptor')
MTLDepthStencilDescriptor = ObjCClass('MTLDepthStencilDescriptor')

MTKViewDelegate = ObjCProtocol('MTKViewDelegate')


class Renderer(
    NSObject,
    protocols=[
      MTKViewDelegate,
    ],
):

  device: 'MTLDevice' = objc_property()
  commandQueue: 'MTLCommandQueue' = objc_property()

  scene: Scene = objc_property()

  samplerState: 'MTLSamplerState?' = objc_property()
  depthStencilState: 'MTLDepthStencilState?' = objc_property()

  @objc_method
  def initWithDevice_(self, device):
    self.device = device
    self.commandQueue = device.newCommandQueue()

    send_super(__class__, self, 'init')

    self.buildSamplerState()
    self.buildDepthStencilState()

    return self

  # --- private
  @objc_method
  def buildSamplerState(self):
    descriptor = MTLSamplerDescriptor.new()
    descriptor.minFilter = MTLSamplerMinMagFilter.linear
    descriptor.magFilter = MTLSamplerMinMagFilter.linear
    samplerState = self.device.newSamplerStateWithDescriptor_(descriptor)

    self.samplerState = samplerState

  @objc_method
  def buildDepthStencilState(self):
    depthStencilDescriptor = MTLDepthStencilDescriptor.new()
    depthStencilDescriptor.depthCompareFunction = MTLCompareFunction.less
    depthStencilDescriptor.depthWriteEnabled = True
    depthStencilState = self.device.newDepthStencilStateWithDescriptor_(
      depthStencilDescriptor)
    self.depthStencilState = depthStencilState

  # --- MTKViewDelegate
  @objc_method
  def mtkView_drawableSizeWillChange_(self, view, size: CGSize):
    try:  # `scene?.`
      self.scene.sceneSizeWillChangeTo_(size)
    except Exception as e:
      print(e)

  @objc_method
  def drawInMTKView_(self, view):
    if not ((drawable := view.currentDrawable) and
            (descriptor := view.currentRenderPassDescriptor)):
      return

    commandBuffer = self.commandQueue.commandBuffer()
    commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
      descriptor)

    deltaTime = 1 / view.preferredFramesPerSecond
    commandEncoder.setFragmentSamplerState_atIndex_(
      self.samplerState,
      0,
    )
    commandEncoder.setDepthStencilState_(self.depthStencilState)

    try:  # `scene?.`
      self.scene.renderWithCommandEncoder_deltaTime_(
        commandEncoder,
        deltaTime,
      )
    except Exception as e:
      print(e)

    commandEncoder.endEncoding()
    commandBuffer.presentDrawable_(drawable)
    commandBuffer.commit()

