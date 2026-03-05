from pyrubicon.objc.api import ObjCProtocol, ObjCInstance
from pyrubicon.objc.api import objc_method, objc_property


class Texturable(metaclass=ObjCProtocol):

  texture: 'MTLTexture?' = objc_property()

  @objc_method
  def setTextureWithDevice_imageName_(self, device, imageName) -> ObjCInstance:
    ...

