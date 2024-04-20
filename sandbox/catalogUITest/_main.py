from pyrubicon.objc.api import ObjCClass, objc_method
from pyrubicon.objc.runtime import send_super

from rbedge.functions import NSStringFromClass
import pdbr

ObjCClass.auto_rename = True

# --- UIViewController
UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

UILabel = ObjCClass('UILabel')
UIFont = ObjCClass('UIFont')
UIColor = ObjCClass('UIColor')

UIView = ObjCClass('UIView')


class MainViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    # --- Navigation
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    # --- View
    backgroundColor = UIColor.systemBackgroundColor()
    self.view.backgroundColor = backgroundColor

    self.label = UILabel.new()
    self.label.text = 'UIKitCatalog'
    self.label.font = UIFont.systemFontOfSize_(26.0)
    self.label.sizeToFit()
    
    uiv = UIView.new()
    uiv.backgroundColor = UIColor.systemOrangeColor()
    

    self.view.addSubview_(self.label)
    self.view.addSubview_(uiv)
    
    # --- Layout
    self.label.translatesAutoresizingMaskIntoConstraints = False
    uiv.translatesAutoresizingMaskIntoConstraints = False

    NSLayoutConstraint.activateConstraints_([
      self.label.centerXAnchor.constraintEqualToAnchor_(
        self.view.centerXAnchor),
      self.label.centerYAnchor.constraintEqualToAnchor_(
        self.view.centerYAnchor),
      uiv.widthAnchor.constraintEqualToAnchor_multiplier_(
        self.view.widthAnchor, 0.5),
      uiv.heightAnchor.constraintEqualToAnchor_multiplier_(
        self.view.heightAnchor, 0.5),
    ])


if __name__ == '__main__':
  from rbedge import present_viewController

  vc = MainViewController.new()
  present_viewController(vc)

