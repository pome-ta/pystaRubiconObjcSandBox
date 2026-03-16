from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSize

from nodes import Node


class Scene(Node):

  device: 'MTLDevice' = objc_property()
  size: CGSize = objc_property(CGSize)

  @objc_method
  def initWithDevice_size_(self, device, size: CGSize):

    self.device = device
    self.size = size
    
    send_super(__class__, self, 'init')

    return self

