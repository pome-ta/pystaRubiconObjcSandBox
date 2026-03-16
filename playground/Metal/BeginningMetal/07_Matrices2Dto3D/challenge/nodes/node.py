from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGFloat

from rbedge.simd import (
  simd_float2,
  simd_float3,
  simd_float4,
  simd_float4x4,
)

from matrixMath import matrix_float4x4


class Node(NSObject):

  name: str = objc_property(object)
  children: ['Node'] = objc_property(object)

  position: 'float3' = objc_property(object)
  rotation: 'float3' = objc_property(object)
  scale: 'float3' = objc_property(object)

  modelMatrix: matrix_float4x4 = objc_property(object)

  @objc_method
  def initializeProperties(self):
    # todo: class member declarations
    self.name = 'Untitled'
    self.children = []

    self.position = simd_float3(0)
    self.rotation = simd_float3(0)
    self.scale = simd_float3(1)

    matrix = matrix_float4x4.translation(self.position.x, self.position.y,
                                         self.position.z)
    matrix = matrix.rotatedBy(self.rotation.x, 1, 0, 0)
    #matrix = matrix.rotatedBy(self.rotation.y, 0, 1, 0)
    #matrix = matrix.rotatedBy(self.rotation.z, 0, 0, 1)
    #matrix = matrix.scaledBy(self.scale.x, self.scale.y, self.scale.z)

    print(matrix)
    print('')

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    self.initializeProperties()

    return self

  @objc_method
  def addChildNode_(self, childNode):
    self.children.append(childNode)

  @objc_method
  def renderWithCommandEncoder_deltaTime_(self, commandEncoder,
                                          deltaTime: CGFloat):
    for child in self.children:
      child.renderWithCommandEncoder_deltaTime_(commandEncoder, deltaTime)

