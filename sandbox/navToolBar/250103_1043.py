import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super, objc_id

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
UIColor = ObjCClass('UIColor')


class ViewController(UIViewController):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print('\tdealloc')
    pass

  # MARK: - View Life Cycle
  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.navigationController.setToolbarHidden_animated_(False, True)

    self.view.backgroundColor = UIColor.systemGreenColor()

    #self.navigationController.setToolbarHidden_animated_(False, True)

    toolbar = self.navigationController.toolbar
    toolbar.setBackgroundColor_(UIColor.systemBlueColor())
    #self.navigationController.toolbar.standardAppearance.setBackgroundColor_(UIColor.systemBlueColor())

    #pdbr.state(self.navigationController.view)
    #print(self.navigationController)
    #print(self.navigationController.view)
    #print(self.view)
    #pdbr.state()
    #print(self.navigationController.toolbar.size.height)
    height = self.navigationController.toolbar.size.height

    #self.view.addSubview_(toolbar)

    layoutMarginsGuide = self.view.layoutMarginsGuide
    #safeAreaLayoutGuide = self.view.safeAreaLayoutGuide
    safeAreaLayoutGuide = self.navigationController.view.safeAreaLayoutGuide
    
    #toolbar.translatesAutoresizingMaskIntoConstraints = False
    '''
    NSLayoutConstraint.activateConstraints_([
      toolbar.bottomAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.bottomAnchor),
      toolbar.leadingAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.leadingAnchor),
      toolbar.trailingAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.trailingAnchor),
      toolbar.heightAnchor.constraintEqualToConstant_(height + 120.0)
    ])
    '''

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print('viewWillAppear')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print('viewDidAppear')
    #pdbr.state(self.navigationController.toolbar)

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print('viewDidDisappear')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'{__class__}: didReceiveMemoryWarning')


if __name__ == '__main__':
  from rbedge.functions import NSStringFromClass
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController

  main_vc = ViewController.new()
  _title = NSStringFromClass(ViewController)
  main_vc.navigationItem.title = _title

  presentation_style = UIModalPresentationStyle.fullScreen
  present_viewController(main_vc, presentation_style)

