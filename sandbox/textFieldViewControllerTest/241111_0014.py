from pyrubicon.objc.api import ObjCClass, ObjCProtocol
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import SEL, send_super, objc_id
from pyrubicon.objc.types import CGRectMake

from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
UITextField = ObjCClass('UITextField')
UITextFieldDelegate = ObjCProtocol('UITextFieldDelegate')

class ViewController(UIViewController,protocols=[
                                UITextFieldDelegate,
                              ]):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    textField = UITextField.alloc().initWithFrame_(
      CGRectMake(77.5, 15.0, 220.0, 34.0)).autorelease()

    textField.backgroundColor = ObjCClass('UIColor').systemRedColor()

    self.view.addSubview_(textField)
    #pdbr.state(textField, 1)
    pdbr.state(textField)
    #print(textField.autocorrectionType)


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController

  main_vc = ViewController.new()
  #style = UIModalPresentationStyle.pageSheet
  style = UIModalPresentationStyle.fullScreen
  present_viewController(main_vc, style)

