from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGFloat

from rbedge.simd import simd_float4

# todo: Pythonista3 の`scene.Scene` ではない
from .scene import Scene
from nodes import Model


class LandscapeScene(Scene):

  sun: Model = objc_property()

  @objc_method
  def initWithDevice_size_(self, device, size: CGSize):
    self.sun = Model.alloc().initWithDevice_modelName_(
      device,
      'sun',
    )

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

