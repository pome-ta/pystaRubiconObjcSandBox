if __name__ == '__main__':
  try:
    import bootstrap

  except ModuleNotFoundError:
    import pathlib, runpy

    _BOOTSTRAP_NAME = 'bootstrap.py'
    '''

    def _bootsetup(file_path: str) -> None:
      _spec = importlib.util.spec_from_file_location(
        _BOOTSTRAP_NAME,
        next((p for _p in pathlib.Path(__file__).resolve().parents
              if (p := _p / _BOOTSTRAP_NAME).is_file()), None))
      _spec.loader.exec_module(importlib.util.module_from_spec(_spec))

    _bootsetup(__file__)
    '''

    try:
      p = next((p for d in pathlib.Path(__file__).resolve().parents
                if (p := d / _BOOTSTRAP_NAME).is_file()), )
    except StopIteration:
      raise FileNotFoundError("...")
    runpy.run_path(p)

#from pyrubicon.objc.api import ObjCClass, ObjCProtocol
#import sys

#/private/var/mobile/Containers/Shared/AppGroup/8407487D-7299-4D3D-BAA4-03D6D8587E48/File Provider Storage/Repositories/pystaRubiconObjcSandBox/playground/modulesBootstrap/app/controls/button/storyboard_buttonViewController.py

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

