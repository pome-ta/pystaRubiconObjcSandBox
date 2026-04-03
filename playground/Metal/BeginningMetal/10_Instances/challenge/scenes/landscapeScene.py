from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGFloat

from rbedge.simd import simd_float4

# todo: Pythonista3 の`scene.Scene` ではない
from .scene import Scene
from nodes import Model, Plane, Instance


class LandscapeScene(Scene):

  sun: Model = objc_property()
  ground: Plane = objc_property()
  grass: Instance = objc_property()
  mushroom: Model = objc_property()

  @objc_method
  def initWithDevice_size_(self, device, size: CGSize):
    self.ground = Plane.alloc().initWithDevice_(device)
    self.grass = Instance.alloc().initWithDevice_modelName_instances_(
      device,
      'grass',
      100,
    )  # 10000
    self.mushroom = Model.alloc().initWithDevice_modelName_(device, 'mushroom')
    self.sun = Model.alloc().initWithDevice_modelName_(device, 'sun')
    send_super(__class__,
               self,
               'initWithDevice:size:',
               device,
               size,
               argtypes=[
                 objc_id,
                 CGSize,
               ])

    self.addChildNode_(self.sun)
    self.sun.materialColor = simd_float4(1.0, 1.0, 0.0, 1.0)
    self.setupScene()

    return self

  @objc_method
  def setupScene(self):
    self.ground.materialColor = simd_float4(0.4, 0.3, 0.1, 1)  # brown
    self.addChildNode_(self.ground)
    self.addChildNode_(self.grass)
    self.addChildNode_(self.mushroom)

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

