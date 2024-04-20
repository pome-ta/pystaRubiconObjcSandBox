from pyrubicon.objc.api import ObjCClass, objc_method
from pyrubicon.objc.runtime import send_super

from rbedge.functions import NSStringFromClass


ObjCClass.auto_rename = True

# --- UIViewController
UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')
UIButtonConfiguration = ObjCClass('UIButtonConfiguration')
UIButton = ObjCClass('UIButton')

NSLayoutConstraint = ObjCClass('NSLayoutConstraint')


class MainViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    # --- Navigation
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    # --- View
    backgroundColor = UIColor.systemBackgroundColor()
    baseBackgroundColor = UIColor.systemOrangeColor()
    baseForegroundColor = UIColor.systemGreenColor()

    self.view.backgroundColor = backgroundColor

    config = UIButtonConfiguration.tintedButtonConfiguration()
    config.title = 'Tap'
    config.baseBackgroundColor = baseBackgroundColor
    config.baseForegroundColor = baseForegroundColor

    tapButton = UIButton.new()
    tapButton.configuration = config

    self.view.addSubview_(tapButton)
    # --- Layout
    tapButton.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      tapButton.centerXAnchor.constraintEqualToAnchor_(
        self.view.centerXAnchor),
      tapButton.centerYAnchor.constraintEqualToAnchor_(
        self.view.centerYAnchor),
      tapButton.widthAnchor.constraintEqualToAnchor_multiplier_(
        self.view.widthAnchor, 0.4),
      tapButton.heightAnchor.constraintEqualToAnchor_multiplier_(
        self.view.heightAnchor, 0.1),
    ])


if __name__ == "__main__":
  from rbedge import present_viewController
  
  vc = MainViewController.new()
  present_viewController(vc)

