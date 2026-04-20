import ctypes

from pyrubicon.objc.api import ObjCProtocol
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSize, CGFloat

from objc_frameworks.Metal import MTLResourceOptions

from nodes import Node, Camera

from simdTypes import SceneConstants, Light


class SceneDelegate(metaclass=ObjCProtocol):

  @objc_method
  def transitionTo_(self, scene):
    ...


class Scene(Node, protocols=[SceneDelegate]):

  device: 'MTLDevice' = objc_property()
  #size: CGSize = objc_property(CGSize)
  _size_storage: CGSize = objc_property(CGSize)

  camera: Camera = objc_property()
  sceneConstants: SceneConstants = objc_property(object)
  light: Light = objc_property(object)

  sceneDelegate: SceneDelegate = objc_property()

  @objc_method
  def size(self) -> CGSize:
    return self._size_storage

  @objc_method
  def setSize_(self, new_size: CGSize):
    self.sceneSizeWillChangeTo_(new_size)
    self._size_storage = new_size

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

  @objc_method
  def touchesBegan_touches_with_(self, view, touches, event):
    pass

  @objc_method
  def touchesMoved_touches_with_(self, view, touches, event):
    pass

  @objc_method
  def touchesEnded_touches_with_(self, view, touches, event):
    pass

  @objc_method
  def touchesCancelled_touches_with_(self, view, touches, event):
    pass

