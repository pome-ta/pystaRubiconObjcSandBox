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
UIToolbar = ObjCClass('UIToolbar')

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
    self.view.backgroundColor = UIColor.systemGreenColor()

    self.navigationController.setToolbarHidden_animated_(False, False)

    toolbar = self.navigationController.toolbar
    #pdbr.state(self.navigationController)
    #pdbr.state(toolbar)
    #print(toolbar.isTranslucent())

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

    #toolbar.setItems_animated_(toolbarButtonItems, True)
    #self.setToolbarItems_animated_(toolbarButtonItems, True)
    #self.view.addSubview_(toolbar)
    #pdbr.state(self)
    #print(self.view._autolayoutTrace())
    #pdbr.state(self.view)
    #self.setToolbarItems_animated_(toolbarButtonItems, True)

    subView = UIView.new()
    subView.backgroundColor = UIColor.systemDarkYellowColor()

    toolSizeView = UIView.new()
    toolSizeView.backgroundColor = UIColor.systemDarkRedColor()

    toolbarSize = toolbar.size
    #toolbarSize.height
    #toolbarSize.width

    #pdbr.state(toolbar.size())

    # --- layout
    layoutMarginsGuide = self.view.layoutMarginsGuide
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    self.view.addSubview_(subView)
    subView.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      subView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      #subView.centerYAnchor.constraintEqualToAnchor_(safeAreaLayoutGuide.centerYAnchor),
      subView.bottomAnchor.constraintEqualToAnchor_(self.view.bottomAnchor),
      subView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor, 0.9),
      subView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor, 1.05),
    ])

    self.view.addSubview_(toolSizeView)
    toolSizeView.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      toolSizeView.widthAnchor.constraintEqualToConstant_(toolbarSize.width),
      toolSizeView.heightAnchor.constraintEqualToConstant_(toolbarSize.height),
      toolSizeView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      toolSizeView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
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

