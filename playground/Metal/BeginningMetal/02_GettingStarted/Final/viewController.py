_TOP_DIR_NAME = 'pystaRubiconObjcSandBox'
_MODULES_DIR_NAME = 'modules'

# todo: `./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME}` にあるpackage のimport 準備
if __name__ == '__main__' and not __file__[:__file__.rfind('/')].endswith(
    _TOP_DIR_NAME):
  import pathlib
  import sys
  __parents = pathlib.Path(__file__).resolve().parents
  for path in __parents:
    if path.name == _TOP_DIR_NAME and (__modules_path :=
                                       path / _MODULES_DIR_NAME).exists():
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
from pyrubicon.objc.runtime import send_super

from objc_frameworks.Foundation import NSStringFromClass

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

from enum import Enum

from pyrubicon.objc.runtime import load_library, NSObject
from pyrubicon.objc.api import objc_const, ObjCInstance

from objc_frameworks.CoreGraphics import CGRectZero

Metal = load_library('Metal')

MTKView = ObjCClass('MTKView')


def MTLCreateSystemDefaultDevice() -> ObjCInstance:
  _function = Metal.MTLCreateSystemDefaultDevice
  _function.restype = ctypes.c_void_p
  return ObjCInstance(_function())


from pyrubicon.objc.types import __LP64__, with_preferred_encoding

_MTLClearColorEncoding = b'{MTLClearColor=dddd}'
'''
@with_preferred_encoding(_MTLClearColorEncoding)
class MTLClearColor(ctypes.Structure):

  _fields_ = [
    ('red', ctypes.c_double),
    ('green', ctypes.c_double),
    ('blue', ctypes.c_double),
    ('alpha', ctypes.c_double),
  ]

  def __repr__(self):
    return f'<MTLClearColor({self.red}, {self.green}, {self.blue}, {self.alpha})>'

  def __str__(self):
    return f'red={self.red}, green={self.green}, blue={self.blue}, alpha={self.alpha}'


def MTLClearColorMake(red: ctypes.c_double, green: ctypes.c_double,
                      blue: ctypes.c_double,
                      alpha: ctypes.c_double) -> MTLClearColor:
  return MTLClearColor(red, green, blue, alpha)


cc = (MTLClearColorMake(0.0, 0.4, 0.21, 1.0))


class Colors(Enum):
  wenderlichGreen = MTLClearColorMake(0.0, 0.4, 0.21, 1.0)
'''


class MainViewController(UIViewController):

  metalView: MTKView = objc_property()
  commandQueue: NSObject = objc_property()

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
    metalView = MTKView.alloc().initWithFrame_device_(CGRectZero, device)

    #metalView.clearColor = Colors.wenderlichGreen
    #metalView.clearColor = (0.0, 0.4, 0.21, 1.0)
    #print(metalView.clearColor)
    #print(Colors.wenderlichGreen)
    #metalView.clearColor = MTLClearColorMake(0.0, 0.4, 0.21, 1.0)
    #metalView.setClearColor_((0.0, 0.4, 0.21, 1.0))
    #pdbr.state(metalView)
    #print(metalView.clearColor)

    #metalView.delegate = self
    commandQueue = device.newCommandQueue()
    pdbr.state(commandQueue)

    self.view.addSubview_(metalView)

    # --- Layout
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    metalView.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      metalView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      metalView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      metalView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor, 0.5),
      metalView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor, 0.5),
    ])

    self.metalView = metalView

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

  # --- MTKViewDelegate
  @objc_method
  def drawInMTKView_(self, view: ctypes.c_void_p):
    print('y')
    pass


if __name__ == '__main__':
  from rbedge.app import App
  from objc_frameworks.UIKit import UIModalPresentationStyle

  main_vc = MainViewController.new()

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()

