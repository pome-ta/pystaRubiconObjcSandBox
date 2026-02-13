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

from pyrubicon.objc.api import ObjCClass, ObjCProtocol
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, autoreleasepool

from objc_frameworks.Foundation import NSStringFromClass

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- Metal
from pyrubicon.objc.api import ObjCProtocol
from pyrubicon.objc.types import CGSize

from objc_frameworks.CoreGraphics import CGRectZero
from objc_frameworks.Metal import MTLCreateSystemDefaultDevice, MTLClearColorMake

MTKView = ObjCClass('MTKView')
MTKViewDelegate = ObjCProtocol('MTKViewDelegate')


class Colors:
  wenderlichGreen = MTLClearColorMake(0.0, 0.4, 0.21, 1.0)


#class MainViewController(UIViewController, protocols=[MTKViewDelegate]):
class MainViewController(UIViewController):
  metalView: MTKView
  commandQueue: 'MTLCommandQueue'

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
    metalView.clearColor = Colors.wenderlichGreen

    metalView.delegate = self
    commandQueue = device.newCommandQueue()

    print('v')
    
    metalView.setPaused_(True)
    metalView.enableSetNeedsDisplay = False
    #metalView.setNeedsDisplay()
    

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
    self.commandQueue = commandQueue

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
    self.metalView.setPaused_(False)

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    self.metalView.setPaused_(True)

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    self.metalView.delegate = None

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'	{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  # --- MTKViewDelegate
  @objc_method
  def mtkView_drawableSizeWillChange_(self, view, size: CGSize):
    pass

  @objc_method
  def drawInMTKView_(self, view):
    with autoreleasepool():
      if not ((drawable := view.currentDrawable) and
              (descriptor := view.currentRenderPassDescriptor)):
        return
  
      commandBuffer = self.commandQueue.commandBuffer()
      commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
        descriptor)
      commandEncoder.endEncoding()
      commandBuffer.presentDrawable_(drawable)
      commandBuffer.commit()


if __name__ == '__main__':
  from rbedge.app import App
  from objc_frameworks.UIKit import UIModalPresentationStyle

  main_vc = MainViewController.new()

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()

