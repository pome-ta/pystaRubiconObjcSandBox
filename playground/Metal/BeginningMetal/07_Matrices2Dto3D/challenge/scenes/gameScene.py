from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGFloat

from rbedge.simd import simd_float3

# todo: Pythonista3 の`scene.Scene` ではない
from .scene import Scene
from nodes import Plane


class GameScene(Scene):

  quad: Plane = objc_property()

  @objc_method
  def initWithDevice_size_(self, device, size: CGSize):

    self.quad = Plane.alloc().initWithDevice_imageName_(device, 'picture.png')

    send_super(__class__,
               self,
               'initWithDevice:size:',
               device,
               size,
               argtypes=[
                 objc_id,
                 CGSize,
               ])

    self.addChildNode_(self.quad)

    quad2 = Plane.alloc().initWithDevice_imageName_(device, 'picture.png')
    quad2.scale = simd_float3(0.5)
    quad2.position.y = 1.5

    self.quad.addChildNode_(quad2)

    return self

  # --- override
  @objc_method
  def updateWithDeltaTime_(self, deltaTime: CGFloat):
    send_super(__class__,
               self,
               'updateWithDeltaTime:',
               deltaTime,
               argtypes=[
                 CGFloat,
               ])

    self.quad.rotation.y += deltaTime

