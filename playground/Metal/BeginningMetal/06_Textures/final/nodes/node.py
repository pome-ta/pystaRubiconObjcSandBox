from pyrubicon.objc.api import NSObject
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGFloat


class Node(NSObject):

  name: str = objc_property(object)
  children: ['Node'] = objc_property(object)

  @objc_method
  def init_properties(self):
    # todo: class member declarations
    self.name = 'Untitled'
    self.children = []

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    self.init_properties()

    return self

  @objc_method
  def addChildNode_(self, childNode):
    self.children.append(childNode)

  @objc_method
  def renderWithCommandEncoder_deltaTime_(self, commandEncoder,
                                          deltaTime: CGFloat):
    for child in self.children:
      child.renderWithCommandEncoder_deltaTime_(commandEncoder, deltaTime)

