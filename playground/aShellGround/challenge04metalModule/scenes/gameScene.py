from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize

# todo: Pythonista3 の`scene.Scene` ではない
from .scene import Scene
from nodes import Plane


class GameScene(Scene):

  quad: Plane = objc_property()

  @objc_method
  def initWithDevice_size_(self, device, size: CGSize):
    send_super(__class__,
               self,
               'initWithDevice:size:',
               device,
               size,
               argtypes=[
                 objc_id,
                 CGSize,
               ])

    self.quad = Plane.alloc().initWithDevice_(device)
    self.addChildNode_(self.quad)

    return self


if __name__ == '__main__':
  pass

