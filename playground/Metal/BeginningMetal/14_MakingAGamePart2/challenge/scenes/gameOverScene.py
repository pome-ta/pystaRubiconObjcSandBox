from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGFloat

# todo: Pythonista3 の`scene.Scene` ではない
from .scene import Scene
from nodes import Model


class GameOverScene(Scene):

  gameOverModel: 'Model!' = objc_property()
  registerTouch: bool = objc_property(object)
  time: float = objc_property(object)
  #win: bool = objc_property(object)
  #_win:bool = objc_ivar(ctypes.c_bool)
  _winStorage: bool = objc_property(bool)

  @objc_method
  def win(self) -> bool:
    return self._winStorage

  @objc_method
  def setWin_(self, new_win: bool):
    self._winStorage = new_win
    print('se')

  @objc_method
  def initializeProperties(self):
    # todo: class member declarations
    send_super(__class__, self, 'initializeProperties')
    self.registerTouch = False
    self.time = 0.0
    #self.win = False
    #set_ivar(self, '_win', False)
    self._winStorage = False

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

