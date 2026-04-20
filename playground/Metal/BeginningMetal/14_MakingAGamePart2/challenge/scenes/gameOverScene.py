import ctypes

from pyrubicon.objc.api import objc_method, objc_property, at
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGFloat

from objc_frameworks.Foundation import NSKeyValueObservingOptions

# todo: Pythonista3 の`scene.Scene` ではない
from .scene import Scene
from nodes import Model


class GameOverScene(Scene):

  gameOverModel: 'Model!' = objc_property()
  registerTouch: bool = objc_property(object)
  time: float = objc_property(object)
  win: bool = objc_property(object)

  @objc_method
  def initializeProperties(self):
    # todo: class member declarations
    send_super(__class__, self, 'initializeProperties')
    self.registerTouch = False
    self.time = 0.0
    self.win = False

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

    #self.addObserver_forKeyPath_options_context_(self, at('win'), NSKeyValueObservingOptions.new, None)

    return self

  
  @objc_method
  def observeValueForKeyPath_ofObject_change_context_(
    self,
    keyPath,
    objct,
    change,
    context,
  ):
    send_super(__class__,
               self,
               'observeValueForKeyPath:ofObject:change:context:',
               keyPath,
               objct,
               change,
               context,
               argtypes=[
                 objc_id,
                 objc_id,
                 objc_id,
                 ctypes.c_void_p,
               ])
    print('ob')
  

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

