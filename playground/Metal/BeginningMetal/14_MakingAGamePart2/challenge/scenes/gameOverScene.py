from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGFloat

# todo: Pythonista3 の`scene.Scene` ではない
from .scene import Scene
from nodes import Model


class GameOverScene(Scene):
  
  gameOverModel: 'Model!' = objc_property()

  @objc_method
  def initializeProperties(self):
    # todo: class member declarations
    send_super(__class__, self, 'initializeProperties')

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
