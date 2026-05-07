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
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSize, UIEdgeInsetsMake

from objc_frameworks.Foundation import NSStringFromClass
from objc_frameworks.CoreGraphics import CGRectZero
from objc_frameworks.UIKit import (
  UILayoutConstraintAxis,
  NSTextAlignment,
  UIViewAutoresizing,
)
from objc_frameworks.Metal import (
  MTLCreateSystemDefaultDevice,
  MTLClearColorMake,
)

from rbedge import pdbr

MTKViewDelegate = ObjCProtocol('MTKViewDelegate')

UIViewController = ObjCClass('UIViewController')
MTKView = ObjCClass('MTKView')
UIStackView = ObjCClass('UIStackView')
UIColor = ObjCClass('UIColor')
UIView = ObjCClass('UIView')


class MainViewController(UIViewController, protocols=[MTKViewDelegate]):

  verticalView: UIStackView = objc_property()
  commandQueue: 'MTLCommandQueue' = objc_property()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.navigationItem.title = NSStringFromClass(__class__)

    device = MTLCreateSystemDefaultDevice()
    commandQueue = device.newCommandQueue()

    #metalView = MTKView.alloc().initWithFrame_device_(CGRectZero, device)
    metalView = MTKView.new()
    metalView.device = device
    #metalView.setDevice_(device)

    metalView.clearColor = MTLClearColorMake(
      red=1,
      green=1,
      blue=0.8,
      alpha=1,
    )

    metalView.delegate = self
    metalView.autoresizingMask = UIViewAutoresizing.flexibleWidth | UIViewAutoresizing.flexibleHeight

    metalView.enableSetNeedsDisplay = True
    metalView.setNeedsDisplay()

    view = UIView.new()
    view.autoresizingMask = UIViewAutoresizing.flexibleWidth | UIViewAutoresizing.flexibleHeight
    view.addSubview_(metalView)

    verticalView = UIStackView.alloc().initWithArrangedSubviews_([
      view,
    ])
    verticalView.layoutMargins = UIEdgeInsetsMake(16.0, 16.0, 16.0, 16.0)
    verticalView.setLayoutMarginsRelativeArrangement_(True)

    verticalView.backgroundColor = UIColor.secondarySystemBackgroundColor()

    self.verticalView = verticalView
    self.commandQueue = commandQueue

    self.setupLayoutConstraint()

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'	{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  # --- private
  @objc_method
  def setupLayoutConstraint(self):
    NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

    self.view.addSubview_(self.verticalView)

    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    self.verticalView.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      self.verticalView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      self.verticalView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      self.verticalView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor,
        0.88,
      ),
      self.verticalView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor,
        0.88,
      ),
    ])

  # --- MTKViewDelegate
  @objc_method
  def mtkView_drawableSizeWillChange_(self, view, size: CGSize):
    pass

  @objc_method
  def drawInMTKView_(self, view):
    print('d')

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

