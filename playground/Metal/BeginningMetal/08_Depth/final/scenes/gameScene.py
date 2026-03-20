from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGFloat

from rbedge.simd import simd_float3

# todo: Pythonista3 の`scene.Scene` ではない
from .scene import Scene
from nodes import Plane, Cube


class GameScene(Scene):

  quad: Plane = objc_property()
  cube: Cube = objc_property()

  @objc_method
  def initWithDevice_size_(self, device, size: CGSize):
    self.cube = Cube.alloc().initWithDevice_(device)
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

    self.addChildNode_(self.cube)
    self.addChildNode_(self.quad)

    self.quad.position.z = -3.0
    self.quad.scale = simd_float3(3.0)

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

