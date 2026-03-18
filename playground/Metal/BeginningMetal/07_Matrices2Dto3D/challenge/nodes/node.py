from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGFloat

from rbedge.simd import simd_float3, matrix_multiply
from rbedge import pdbr

from .renderable import Renderable
from matrixMath import matrix_float4x4


class Node(NSObject):

  name: str = objc_property(object)
  children: ['Node'] = objc_property(object)

  position: 'float3' = objc_property(object)
  rotation: 'float3' = objc_property(object)
  scale: 'float3' = objc_property(object)

  #modelMatrix: matrix_float4x4 = objc_property(object)
  #_modelMatrixValue: matrix_float4x4 = objc_property(object)

  @objc_method  # declare_property - getter
  def modelMatrix(self) -> object:
    matrix = matrix_float4x4.translation(self.position.x, self.position.y,
                                         self.position.z)

    matrix = matrix.rotatedBy(self.rotation.x, 1, 0, 0)
    matrix = matrix.rotatedBy(self.rotation.y, 0, 1, 0)
    matrix = matrix.rotatedBy(self.rotation.z, 0, 0, 1)
    matrix = matrix.scaledBy(self.scale.x, self.scale.y, self.scale.z)
    #self._modelMatrixValue = matrix
    return matrix

  '''
  @objc_method  # setter
  def setModelMatrix_(self, modelMatrixValue: object):
    #self._modelMatrixValue = modelMatrixValue
    pass
  '''
  @objc_method
  def initializeProperties(self):
    # todo: class member declarations
    self.name = 'Untitled'
    self.children = []

    self.position = simd_float3(0)
    self.rotation = simd_float3(0)
    #self.position = simd_float3(0.25)
    #self.rotation = simd_float3(0.7)
    self.scale = simd_float3(1)
    
    #self.declare_property('modelMatrix')
    __class__.declare_property('modelMatrix')
    
    
    '''

    matrix = matrix_float4x4.translation(self.position.x, self.position.y,
                                         self.position.z)

    matrix = matrix.rotatedBy(self.rotation.x, 1, 0, 0)
    matrix = matrix.rotatedBy(self.rotation.y, 0, 1, 0)
    matrix = matrix.rotatedBy(self.rotation.z, 0, 0, 1)
    matrix = matrix.scaledBy(self.scale.x, self.scale.y, self.scale.z)
    '''

    #self.modelMatrix = matrix
    #self.modelMatrix = self.modelMatrix
    #self.modelMatrixaa = matrix

    #print(self.modelMatrixaa)

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    self.initializeProperties()

    return self

  @objc_method
  def addChildNode_(self, childNode):
    #print(f'childNode: {childNode}')
    self.children.append(childNode)

  @objc_method
  def renderWithCommandEncoder_parentModelViewMatrix_(
      self, commandEncoder, parentModelViewMatrix: object):
    modelViewMatrix = matrix_multiply(parentModelViewMatrix, self.modelMatrix)

    #print(self.name)
    #print(dir(modelViewMatrix))
    #print(modelViewMatrix)

    for child in self.children:
      #print(f'{child.name}')
      child.renderWithCommandEncoder_parentModelViewMatrix_(
        commandEncoder, modelViewMatrix)

    if self.conformsToProtocol_(Renderable) and (renderable := self):
      commandEncoder.pushDebugGroup_(self.name)
      renderable.doRenderWithCommandEncoder_modelViewMatrix_(
        commandEncoder, modelViewMatrix)
      commandEncoder.popDebugGroup()

  '''
  @objc_method
  def renderWithCommandEncoder_deltaTime_(self, commandEncoder,
                                          deltaTime: CGFloat):
    for child in self.children:
      child.renderWithCommandEncoder_deltaTime_(commandEncoder, deltaTime)
  '''

#Node.declare_property('modelMatrix')
