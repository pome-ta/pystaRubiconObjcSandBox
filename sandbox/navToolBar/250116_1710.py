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

UIToolbarAppearance = ObjCClass('UIToolbarAppearance')
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

    toolbarAppearance = UIToolbarAppearance.new()
    toolbarAppearance.configureWithDefaultBackground()
    #toolbarAppearance.configureWithOpaqueBackground()
    #toolbarAppearance.configureWithTransparentBackground()
    #pdbr.state(toolbarAppearance)
    #toolbarAppearance.setBackgroundColor_(UIColor.systemDarkYellowColor())

    #navToolbar = self.navigationController.toolbar
    toolbar = self.navigationController.toolbar

    #toolbar = UIToolbar.alloc().initWithFrame_(navToolbar.frame)
    #toolbar.setAutoresizingMask_(navToolbar.autoresizingMask)
    #autoresizingMask
    #frame
    '''
    
    toolbar.standardAppearance = toolbarAppearance
    toolbar.scrollEdgeAppearance = toolbarAppearance
    toolbar.compactAppearance = toolbarAppearance
    toolbar.compactScrollEdgeAppearance = toolbarAppearance
    '''

    #toolbar.setBarStyle_(1)
    #toolbar.setTranslucent_(False)
    #toolbar.setTintColor_(UIColor.systemDarkYellowColor())

    #pdbr.state(self.navigationController)
    #pdbr.state(toolbar)

    #setToolbarItems_animated_
    #setToolbarHidden_animated_
    #setToolbar_

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

    #self.navigationController.setToolbar_(toolbar)

    #self.navigationController.setToolbarHidden_animated_(False, True)
    self.navigationController.setToolbarHidden_(False)
    #self.navigationController.setToolbarItems_animated_(toolbarButtonItems, True)
    self.navigationController.setToolbarItems_(toolbarButtonItems)

    #self.setToolbarItems_animated_(toolbarButtonItems, True)

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

