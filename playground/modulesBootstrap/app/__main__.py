if __name__ == '__main__':
  try:
    import bootstrap

  except ModuleNotFoundError:
    import pathlib, runpy

    _SCRIPT_NAME = 'bootstrap.py'
    try:
      next(_script_path for _dir in pathlib.Path(__file__).resolve().parents
           if (_script_path := _dir / _SCRIPT_NAME).is_file())
    except StopIteration:
      raise FileNotFoundError(f'{_SCRIPT_NAME} not found')

    runpy.run_path(_script_path)

#from pyrubicon.objc.api import ObjCClass, ObjCProtocol
#import sys

#[print(f'{p}\n') for p in sys.modules]
'''
for p in sys.modules:
  print(p)
  print('')
'''

import ctypes

from pyrubicon.objc import (
  ObjCClass,
  objc_method,
  objc_property,
)  # api
from pyrubicon.objc import send_super  # runtime

from objc_frameworks.Foundation import NSStringFromClass

from rbedge import pdbr

from controls.button import storyboard_buttonViewController

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

UIColor = ObjCClass('UIColor')


class MainViewController(UIViewController):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t - {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.navigationItem.title = NSStringFromClass(__class__)

    self.view.backgroundColor = UIColor.secondarySystemBackgroundColor()

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
    print(f'\t - {NSStringFromClass(__class__)}: viewDidDisappear')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'\t{NSStringFromClass(__class__)}: didReceiveMemoryWarning')


if __name__ == '__main__':
  from rbedge.app import App
  from objc_frameworks.UIKit import UIModalPresentationStyle

  main_vc = MainViewController.new()

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()

