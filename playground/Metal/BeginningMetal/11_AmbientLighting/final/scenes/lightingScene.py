import ctypes

from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGFloat

from rbedge.simd import simd_float3, simd_float4

# todo: Pythonista3 の`scene.Scene` ではない
from .scene import Scene
from nodes import Model


class LightingScene(Scene):

  mushroom: Model = objc_property()

  @objc_method
  def initWithDevice_size_(self, device, size: CGSize):
    self.mushroom = Model.alloc().initWithDevice_modelName_(device, 'mushroom')

    send_super(__class__,
               self,
               'initWithDevice:size:',
               device,
               size,
               argtypes=[
                 objc_id,
                 CGSize,
               ])

    self.mushroom.position.y = -1
    self.addChildNode_(self.mushroom)

    self.light.color = (ctypes.c_float * 3)(0.0, 0.0, 1.0)
    self.light.ambientIntensity = 0.1

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

