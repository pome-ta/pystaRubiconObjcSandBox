from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSize, CGFloat

from nodes import Node
from matrixMath import matrix_float4x4


class Scene(Node):

  device: 'MTLDevice' = objc_property()
  size: CGSize = objc_property(CGSize)

  @objc_method
  def initWithDevice_size_(self, device, size: CGSize):

    self.device = device
    self.size = size

    send_super(__class__, self, 'init')

    return self

  @objc_method
  def updateWithDeltaTime_(self, deltaTime: CGFloat):
    pass

  @objc_method
  def renderWithCommandEncoder_deltaTime_(self, commandEncoder,
                                          deltaTime: CGFloat):
    self.updateWithDeltaTime_(deltaTime)
    viewMatrix = matrix_float4x4.translation(0.0, 0.0, -4.0)
    for child in self.children:
      child.renderWithCommandEncoder_parentModelViewMatrix_(
        commandEncoder, viewMatrix)

