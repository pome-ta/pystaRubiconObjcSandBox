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
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSize, UIEdgeInsetsMake

from objc_frameworks.Foundation import NSStringFromClass
from objc_frameworks.UIKit import (
  UILayoutConstraintAxis,
  NSTextAlignment,
)

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')

UIStackView = ObjCClass('UIStackView')
UILabel = ObjCClass('UILabel')

UIColor = ObjCClass('UIColor')
UIView = ObjCClass('UIView')


class MainViewController(UIViewController):

  verticalView: UIStackView = objc_property()
  #metalView: UIView = objc_property()
  #text: UILabel = objc_property()

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

    metalView = UIView.new()
    metalView.layer.borderWidth = 1.0
    metalView.layer.borderColor = UIColor.labelColor().CGColor
    #separatorColor
    metalView.backgroundColor = UIColor.systemDarkRedColor()

    text = UILabel.new()
    text.text = 'Hello, Metal!'
    text.textAlignment = NSTextAlignment.center
    #text.backgroundColor = UIColor.systemDarkOrangeColor()

    verticalView = UIStackView.alloc().initWithArrangedSubviews_([
      metalView,
      text,
    ])

    verticalView.axis = UILayoutConstraintAxis.vertical
    #verticalView.spacing = 16.0
    verticalView.layoutMargins = UIEdgeInsetsMake(16.0, 16.0, 16.0, 16.0)
    verticalView.setLayoutMarginsRelativeArrangement_(True)

    verticalView.backgroundColor = UIColor.systemFillColor()
    #systemBackgroundColor

    self.verticalView = verticalView

    self.setupLayoutConstraint()

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


if __name__ == '__main__':
  from rbedge.app import App
  from objc_frameworks.UIKit import UIModalPresentationStyle

  main_vc = MainViewController.new()

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()

