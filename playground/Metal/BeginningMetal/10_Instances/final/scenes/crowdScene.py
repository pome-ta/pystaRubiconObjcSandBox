from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGFloat

from rbedge.simd import simd_float3, simd_float4
from rbedge.stdlib import arc4random_uniform, drand48

# todo: Pythonista3 の`scene.Scene` ではない
from .scene import Scene
from nodes import Model


class CrowdScene(Scene):

  humans: '[Model]' = objc_property(object)

  @objc_method
  def initializeProperties(self):
    # todo: class member declarations
    send_super(__class__, self, 'initializeProperties')
    self.humans = []

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

    self.initializeProperties()

    for _ in range(40):
      human = Model.alloc().initWithDevice_modelName_(device, 'humanFigure')
      self.humans.append(human)
      self.addChildNode_(human)
      human.scale = simd_float3(arc4random_uniform(5) / 10)
      human.position.x = float(arc4random_uniform(5)) - 2
      human.position.y = float(arc4random_uniform(5)) - 3
      human.materialColor = simd_float4(drand48(), drand48(), drand48(), 1.0)

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

