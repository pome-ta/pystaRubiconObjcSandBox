from math import radians

from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGFloat

from rbedge.simd import simd_float3, simd_float4
from rbedge.stdlib import arc4random_uniform

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
      10000,
    )
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

    self.ground.scale = simd_float3(20)
    self.ground.rotation.x = radians(90)

    self.camera.rotation.x = radians(-10)
    self.camera.position.z = -20
    self.camera.position.y = -2

    greens = [
      simd_float4(0.34, 0.51, 0.01, 1),
      simd_float4(0.5, 0.5, 0, 1),
      simd_float4(0.29, 0.36, 0.14, 1),
    ]
    for row in range(100):
      for column in range(100):
        position = simd_float3(0)
        position.x = float(row) / 4
        position.z = float(column) / 4

        blade = self.grass.nodes[row * 100 + column]
        blade.scale = simd_float3(0.5)
        blade.position = position

        blade.materialColor = greens[int(arc4random_uniform(3))]
        blade.rotation.y = radians(float(arc4random_uniform(360)))

    self.grass.position.x = -12
    self.grass.position.z = -12
    self.mushroom.position.x = -6
    self.mushroom.position.z = -8
    self.mushroom.scale = simd_float3(2)

    self.sun.position.y = 7
    self.sun.position.x = 6
    self.sun.scale = simd_float3(2)

    #self.camera.fovDegrees = 25

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

