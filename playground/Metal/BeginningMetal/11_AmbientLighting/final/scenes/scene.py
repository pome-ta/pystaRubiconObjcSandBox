import ctypes

from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSize, CGFloat

from objc_frameworks.Metal import MTLResourceOptions

from nodes import Node, Camera

from simdTypes import SceneConstants, Light


class Scene(Node):

  device: 'MTLDevice' = objc_property()
  size: CGSize = objc_property(CGSize)

  camera: Camera = objc_property()
  sceneConstants: SceneConstants = objc_property(object)
  light: Light = objc_property(object)

  lightBuffer: 'ctypes.c_char_Array_32' = objc_property(object)

  @objc_method
  def initializeProperties(self):
    # todo: class member declarations
    send_super(__class__, self, 'initializeProperties')
    self.camera = Camera.new()
    self.sceneConstants = SceneConstants()
    self.light = Light()

  @objc_method
  def initWithDevice_size_(self, device, size: CGSize):
    self.initializeProperties()

    self.device = device
    self.size = size

    send_super(__class__, self, 'init')

    self.camera.position.z = -6.0
    self.addChildNode_(self.camera)

    return self

  @objc_method
  def updateWithDeltaTime_(self, deltaTime: CGFloat):
    pass

  @objc_method
  def renderWithCommandEncoder_deltaTime_(
    self,
    commandEncoder,
    deltaTime: CGFloat,
  ):
    self.updateWithDeltaTime_(deltaTime)

    self.sceneConstants.projectionMatrix = self.camera.projectionMatrix

    commandEncoder.setFragmentBytes_length_atIndex_(
      self.light.raw,
      Light.stride,
      3,
    )

    commandEncoder.setVertexBytes_length_atIndex_(
      ctypes.byref(self.sceneConstants),
      ctypes.sizeof(SceneConstants),
      2,
    )

    for child in self.children:
      child.renderWithCommandEncoder_parentModelViewMatrix_(
        commandEncoder,
        self.camera.viewMatrix,
      )

  @objc_method
  def sceneSizeWillChangeTo_(self, size: CGSize):
    self.camera.aspect = float(size.width / size.height)

