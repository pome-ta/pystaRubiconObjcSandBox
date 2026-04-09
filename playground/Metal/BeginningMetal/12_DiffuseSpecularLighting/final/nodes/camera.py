from math import radians

from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super

from rbedge.utils import readonly_properties
from rbedge.simd import matrix_multiply

from .node import Node

from matrixMath import matrix_float4x4


@readonly_properties('fovRadians', 'viewMatrix', 'projectionMatrix')
class Camera(Node):

  fovDegrees: float = objc_property(object)
  aspect: float = objc_property(object)
  nearZ: float = objc_property(object)
  farZ: float = objc_property(object)

  @objc_method  # declare_property - getter
  def fovRadians(self) -> object:
    return radians(self.fovDegrees)

  @objc_method  # declare_property - getter
  def viewMatrix(self) -> object:
    return self.modelMatrix

  @objc_method  # declare_property - getter
  def projectionMatrix(self) -> object:
    return matrix_float4x4.projectionFov(
      self.fovRadians,
      self.aspect,
      self.nearZ,
      self.farZ,
    )

  @objc_method
  def initializeProperties(self):
    # todo: class member declarations
    send_super(__class__, self, 'initializeProperties')

    self.fovDegrees = 65.0
    self.aspect = 1.0
    self.nearZ = 0.1
    self.farZ = 100.0

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    self.initializeProperties()

    return self

