_TOP_DIR_NAME = 'pystaRubiconObjcSandBox'
_MODULES_DIR_NAME = 'modules'

# todo: `./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME}` にあるpackage のimport 準備
if __name__ == '__main__' and not __file__[:__file__.rfind('/')].endswith(
    _TOP_DIR_NAME):
  import pathlib
  import sys
  __parents = pathlib.Path(__file__).resolve().parents
  for __dir_path in __parents:
    if __dir_path.name == _TOP_DIR_NAME and (__modules_path := __dir_path /
                                             _MODULES_DIR_NAME).exists():
      sys.path.insert(0, str(__modules_path))
      break
  else:
    import warnings
    with warnings.catch_warnings():
      warnings.simplefilter('always', ImportWarning)
      __warning_message = f'./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME} not found in parent directories'
      warnings.warn(__warning_message, ImportWarning)

import ctypes

from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGSize, CGPoint, CGRect

from objc_frameworks.Foundation import NSStringFromClass

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- Metal
from objc_frameworks.CoreGraphics import CGRectZero
from objc_frameworks.Metal import (
  MTLCreateSystemDefaultDevice,
  MTLClearColorMake,
)

from renderer import Renderer
from scenes import LightingScene

MTKView = ObjCClass('MTKView')

# --- touches event debug
UIView = ObjCClass('UIView')
UIColor = ObjCClass('UIColor')


class Colors:
  wenderlichGreen = MTLClearColorMake(0.0, 0.4, 0.21, 1.0)
  skyBlue = MTLClearColorMake(0.66, 0.9, 0.96, 1.0)


class MainViewController(UIViewController):

  metalView: MTKView = objc_property()
  renderer: Renderer = objc_property()

  debugCircle: UIView = objc_property()

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'	 - {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.navigationItem.title = NSStringFromClass(__class__)

    device = MTLCreateSystemDefaultDevice()
    metalView = MTKView.alloc().initWithFrame_device_(
      self.view.bounds,
      device,
    )

    renderer = Renderer.alloc().initWithDevice_(device)
    renderer.scene = LightingScene.alloc().initWithDevice_size_(
      device,
      metalView.bounds.size,
    )

    metalView.clearColor = Colors.wenderlichGreen
    metalView.delegate = renderer

    #metalView.enableSetNeedsDisplay = True
    #metalView.setNeedsDisplay()

    self.view.addSubview_(metalView)

    self.metalView = metalView
    self.renderer = renderer
    self.setupLayoutConstraint()

    self.debugCircle = None

  @objc_method
  def touchesBegan_withEvent_(self, touches, event):
    send_super(__class__,
               self,
               'touchesBegan:withEvent:',
               touches,
               event,
               argtypes=[
                 objc_id,
                 objc_id,
               ])
    try:  # `renderer?.scene?.`
      self.renderer.scene.touchesBegan_touches_with_(self.view, touches, event)
    except Exception as e:
      print(e)

    if (touch := touches.anyObject()) is None:
      return

    if getattr(self, 'debugCircle', None):
      self.debugCircle.removeFromSuperview()

    location = touch.locationInView_(self.view)
    radius = 25.0
    frame = CGRect(
      CGPoint(location.x - radius, location.y - radius),
      CGSize(radius * 2, radius * 2),
    )
    self.debugCircle = UIView.alloc().initWithFrame_(frame)
    self.debugCircle.backgroundColor = UIColor.redColor.colorWithAlphaComponent_(
      0.5)
    self.debugCircle.layer.cornerRadius = radius
    self.debugCircle.userInteractionEnabled = False

    self.view.addSubview_(self.debugCircle)

  @objc_method
  def touchesMoved_withEvent_(self, touches, event):
    send_super(__class__,
               self,
               'touchesMoved:withEvent:',
               touches,
               event,
               argtypes=[
                 objc_id,
                 objc_id,
               ])
    try:  # `renderer?.scene?.`
      self.renderer.scene.touchesMoved_touches_with_(self.view, touches, event)
    except Exception as e:
      print(e)

    if not getattr(self, 'debugCircle', None):
      return

    if (touch := touches.anyObject()) is None:
      return

    self.debugCircle.center = touch.locationInView_(self.view)

  @objc_method
  def touchesEnded_withEvent_(self, touches, event):
    send_super(__class__,
               self,
               'touchesEnded:withEvent:',
               touches,
               event,
               argtypes=[
                 objc_id,
                 objc_id,
               ])
    try:  # `renderer?.scene?.`
      self.renderer.scene.touchesEnded_touches_with_(self.view, touches, event)
    except Exception as e:
      print(e)
    '''
    if getattr(self, 'debugCircle', None):
      self.debugCircle.removeFromSuperview()
    '''
    self._removeDebugCircle()

  @objc_method
  def touchesCancelled_withEvent_(self, touches, event):
    send_super(__class__,
               self,
               'touchesCancelled:withEvent:',
               touches,
               event,
               argtypes=[
                 objc_id,
                 objc_id,
               ])
    try:  # `renderer?.scene?.`
      self.renderer.scene.touchesCancelled_touches_with_(
        self.view, touches, event)
    except Exception as e:
      print(e)
    '''
    if getattr(self, 'debugCircle', None):
      self.debugCircle.removeFromSuperview()
    '''
    self._removeDebugCircle()

  @objc_method
  def _removeDebugCircle(self):
    if getattr(self, 'debugCircle', None):
      self.debugCircle.removeFromSuperview()

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'	{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  # --- private
  @objc_method
  def setupLayoutConstraint(self):
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    self.metalView.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      self.metalView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      self.metalView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      self.metalView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor,
        0.88,
      ),
      self.metalView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor,
        0.88,
      ),
    ])


if __name__ == '__main__':
  from rbedge.app import App
  from objc_frameworks.UIKit import UIModalPresentationStyle

  main_vc = MainViewController.new()

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()

