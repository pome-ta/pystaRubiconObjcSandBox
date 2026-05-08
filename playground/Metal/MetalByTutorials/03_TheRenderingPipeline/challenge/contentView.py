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

from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import UIEdgeInsetsMake

from objc_frameworks.UIKit import (
  UILayoutConstraintAxis,
  NSTextAlignment,
  UIViewAutoresizing,
)

from rbedge import pdbr

from metalView import MetalView

UIView = ObjCClass('UIView')
UIStackView = ObjCClass('UIStackView')
UILabel = ObjCClass('UILabel')

UIColor = ObjCClass('UIColor')

class ContentView(UIView):

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')

    self.setup()
    return self

  @objc_method
  def setup(self):

    metalView = MetalView.new()
    metalView.layer.borderWidth = 2.0
    metalView.layer.borderColor = UIColor.separatorColor().CGColor

    text = UILabel.new()
    text.text = 'Hello, Metal!'
    text.textAlignment = NSTextAlignment.center

    verticalView = UIStackView.alloc().initWithArrangedSubviews_([
      metalView,
      text,
    ])

    verticalView.axis = UILayoutConstraintAxis.vertical
    #verticalView.spacing = 16.0
    verticalView.layoutMargins = UIEdgeInsetsMake(16.0, 16.0, 16.0, 16.0)
    verticalView.setLayoutMarginsRelativeArrangement_(True)

    verticalView.backgroundColor = UIColor.secondarySystemBackgroundColor()

    verticalView.autoresizingMask = UIViewAutoresizing.flexibleWidth | UIViewAutoresizing.flexibleHeight

    self.addSubview_(verticalView)


if __name__ == '__main__':

  from objc_frameworks.Foundation import NSStringFromClass
  from objc_frameworks.UIKit import UIModalPresentationStyle

  from rbedge.app import App

  UIViewController = ObjCClass('UIViewController')

  class TestContentViewController(UIViewController):

    contentView: ContentView = objc_property()

    @objc_method
    def viewDidLoad(self):
      send_super(__class__, self, 'viewDidLoad')
      self.navigationItem.title = NSStringFromClass(__class__)

      self.contentView = ContentView.new()

      self.setupLayoutConstraint()

    @objc_method
    def didReceiveMemoryWarning(self):
      send_super(__class__, self, 'didReceiveMemoryWarning')
      print(f'	{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

    # --- private
    @objc_method
    def setupLayoutConstraint(self):
      NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

      self.view.addSubview_(self.contentView)

      safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

      self.contentView.translatesAutoresizingMaskIntoConstraints = False

      centerXAnchor = self.contentView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor)
      centerYAnchor = self.contentView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor)

      widthAnchor = self.contentView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor,
        0.88,
      )
      heightAnchor = self.contentView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor,
        0.88,
      )

      NSLayoutConstraint.activateConstraints_([
        centerXAnchor,
        centerYAnchor,
        widthAnchor,
        heightAnchor,
      ])

  main_vc = TestContentViewController.new()

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()

