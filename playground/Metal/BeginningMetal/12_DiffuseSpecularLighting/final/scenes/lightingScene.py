from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGFloat, CGPoint

from rbedge.simd import simd_float3

# todo: Pythonista3 の`scene.Scene` ではない
from .scene import Scene
from nodes import Model


class LightingScene(Scene):

  mushroom: Model = objc_property()
  previousTouchLocation: CGPoint = objc_property(object)

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

    self.light.color = simd_float3(1.0, 1.0, 1.0)
    self.light.ambientIntensity = 0.2
    self.light.diffuseIntensity = 0.8
    self.light.direction = simd_float3(0.0, 0.0, -1.0)

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

  @objc_method
  def touchesBegan_touches_with_(self, view, touches, event):

    send_super(__class__,
               self,
               'touchesBegan:touches:with:',
               view,
               touches,
               event,
               argtypes=[
                 objc_id,
                 objc_id,
                 objc_id,
               ])

    if (touch := touches.anyObject()) is None:
      return
    self.previousTouchLocation = touch.locationInView_(view)

  @objc_method
  def touchesMoved_touches_with_(self, view, touches, event):

    send_super(__class__,
               self,
               'touchesMoved:touches:with:',
               view,
               touches,
               event,
               argtypes=[
                 objc_id,
                 objc_id,
                 objc_id,
               ])

    if (touch := touches.anyObject()) is None:
      return
    touchLocation = touch.locationInView_(view)

    delta = CGPoint(self.previousTouchLocation.x - touchLocation.x,
                    self.previousTouchLocation.y - touchLocation.y)
    sensitivity = 0.01
    self.mushroom.rotation.x += float(delta.y) * sensitivity
    self.mushroom.rotation.y += float(delta.x) * sensitivity
    self.previousTouchLocation = touchLocation

