import ctypes
from pathlib import Path

from pyrubicon.objc.api import ObjCClass, ObjCInstance, NSData
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super, objc_id

from rbedge.enumerations import (
  UIBarStyle,
  UIBarButtonSystemItem,
  UIBarPosition,
  UIBarMetrics,
)

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
UIColor = ObjCClass('UIColor')
UIImage = ObjCClass('UIImage')
NSURL = ObjCClass('NSURL')
UIScreen = ObjCClass('UIScreen')
UIBarButtonItem = ObjCClass('UIBarButtonItem')

UIView = ObjCClass('UIView')


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

    #self.view.backgroundColor = UIColor.systemGreenColor()
    self.navigationController.setToolbarHidden_animated_(False, False)

    # Note that there's no target/action since this represents empty space.
    trashBarButtonItem = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(UIBarButtonSystemItem.trash,
                                                 None, None)
    flexibleSpaceBarButtonItem = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(
      UIBarButtonSystemItem.flexibleSpace, None, None)
    doneBarButtonItem = UIBarButtonItem.alloc(
    ).initWithBarButtonSystemItem_target_action_(UIBarButtonSystemItem.done,
                                                 None, None)

    toolbarButtonItems = [
      trashBarButtonItem,
      flexibleSpaceBarButtonItem,
      doneBarButtonItem,
    ]

    subView = UIView.new()
    subView.backgroundColor = UIColor.systemGreenColor()

    # --- layout
    layoutMarginsGuide = self.view.layoutMarginsGuide
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    self.view.addSubview_(subView)
    subView.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      subView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      subView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      subView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor, 0.9),
      subView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor, 1.05),
    ])

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

