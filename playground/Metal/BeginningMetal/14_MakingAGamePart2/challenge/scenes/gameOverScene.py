from math import sin, pi

from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGFloat

from rbedge.simd import simd_float3, simd_float4

# todo: Pythonista3 の`scene.Scene` ではない
from .scene import Scene
from nodes import Model


class GameOverScene(Scene):

  gameOverModel: 'Model!' = objc_property()
  registerTouch: bool = objc_property(object)
  time: float = objc_property(object)
  _win_storage: bool = objc_property(bool)

  @objc_method
  def win(self) -> bool:
    return self._win_storage

  @objc_method
  def setWin_(self, new_win: bool):
    
    if new_win:
      self.gameOverModel = Model.alloc().initWithDevice_modelName_(
        self.device,
        'youwin',
      )
      self.gameOverModel.materialColor = simd_float4(0, 1, 0, 1)
    else:
      self.gameOverModel = Model.alloc().initWithDevice_modelName_(
        self.device,
        'youlose',
      )
      self.gameOverModel.materialColor = simd_float4(1, 0, 1, 1)

    self.addChildNode_(self.gameOverModel)
    self._win_storage = new_win

  @objc_method
  def initializeProperties(self):
    # todo: class member declarations
    send_super(__class__, self, 'initializeProperties')
    self.registerTouch = False
    self.time = 0.0
    self._win_storage = False

  @objc_method
  def initWithDevice_size_(self, device, size: CGSize):
    self.initializeProperties()
    send_super(__class__,
               self,
               'initWithDevice:size:',
               device,
               size,
               argtypes=[
                 objc_id,
                 CGSize,
               ])

    self.light.color = simd_float3(1, 1, 1)
    self.light.ambientIntensity = 0.3
    self.light.diffuseIntensity = 0.8
    self.light.direction = simd_float3(0, -1, -1)
    self.camera.position.z = -30

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

    self.time += deltaTime

    amplitude: float = 0.5
    period: float = 2.0

    periodicAmount = sin(float(self.time + 0.8) * period) * amplitude * deltaTime

    self.gameOverModel.rotation.x -= pi * periodicAmount
    self.gameOverModel.scale += simd_float3(periodicAmount / 4)

