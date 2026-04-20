from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGFloat

from objc_frameworks.Foundation import NSKeyValueObservingOptions

# todo: Pythonista3 の`scene.Scene` ではない
from .scene import Scene
from nodes import Model


class GameOverScene(Scene):
  
  gameOverModel: 'Model!' = objc_property()
  registerTouch:bool = objc_property(object)
  time:float = objc_property(object)
  win:bool = objc_property(object)

  @objc_method
  def initializeProperties(self):
    # todo: class member declarations
    send_super(__class__, self, 'initializeProperties')
    self.registerTouch = False
    self.time = 0.0
    self.win = False
    
    
    #setRegisterTouch_

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

  @objc_method
  def observeValueForKeyPath_ofObject_change_context_(self, keyPath, objct,
                                                      change, context):
    fractionCompleted = self.progress.fractionCompleted
    # Update the progress views.
    [
      progressView.setProgress_animated_(fractionCompleted, True)
      for progressView in self.progressViews
    ]


  '''
  @objc_method
  def setRegisterTouch_(self, isBool:object):
    return isBool
  '''
  
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
