from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGFloat

from rbedge.utils import readonly_properties
from rbedge.simd import simd_float3, simd_float4, matrix_multiply

from .renderable import Renderable
from matrixMath import matrix_float4x4


@readonly_properties('modelMatrix')
class Node(NSObject):

  name: str = objc_property(object)
  materialColor: 'float4' = objc_property(object)
  specularIntensity: float = objc_property(object)
  shininess: float = objc_property(object)

  children: ['Node'] = objc_property(object)

  position: 'float3' = objc_property(object)
  rotation: 'float3' = objc_property(object)
  scale: 'float3' = objc_property(object)

  #width: float = objc_property(object)
  #height: float = objc_property(object)

  @objc_method  # declare_property - getter
  def modelMatrix(self) -> object:
    matrix = matrix_float4x4.translation(self.position.x, self.position.y,
                                         self.position.z)

    matrix = matrix.rotatedBy(self.rotation.x, 1, 0, 0)
    matrix = matrix.rotatedBy(self.rotation.y, 0, 1, 0)
    matrix = matrix.rotatedBy(self.rotation.z, 0, 0, 1)
    matrix = matrix.scaledBy(self.scale.x, self.scale.y, self.scale.z)

    return matrix

  @objc_method
  def initializeProperties(self):
    # todo: class member declarations
    self.name = 'Untitled'
    self.materialColor = simd_float4(1)
    self.specularIntensity = 1.0
    self.shininess = 1.0

    self.children = []

    self.position = simd_float3(0)
    self.rotation = simd_float3(0)
    self.scale = simd_float3(1)

    #self.width = 1.0
    #self.height = 1.0

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    self.initializeProperties()

    return self

  @objc_method
  def addChildNode_(self, childNode):
    self.children.append(childNode)

  @objc_method
  def renderWithCommandEncoder_parentModelViewMatrix_(
      self, commandEncoder, parentModelViewMatrix: object):
    modelViewMatrix = matrix_multiply(
      parentModelViewMatrix,
      self.modelMatrix,
    )

    for child in self.children:
      child.renderWithCommandEncoder_parentModelViewMatrix_(
        commandEncoder, modelViewMatrix)

    if self.conformsToProtocol_(Renderable) and (renderable := self):
      commandEncoder.pushDebugGroup_(self.name)
      renderable.doRenderWithCommandEncoder_modelViewMatrix_(
        commandEncoder,
        modelViewMatrix,
      )
      commandEncoder.popDebugGroup()

