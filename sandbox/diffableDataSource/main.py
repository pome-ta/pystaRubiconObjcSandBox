""" note: 再度挑戦
[UICollectionViewでUITableViewのようなUIを実現する。ただし#available(iOS 14.0, *) #Swift - Qiita](https://qiita.com/sohichiro/items/9a3394551b8d76d2a346)
"""

import ctypes

from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGRectMake

from rbedge.enumerations import (
  UICollectionLayoutListAppearance, )

from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
UIColor = ObjCClass('UIColor')

UICollectionView = ObjCClass('UICollectionView')
UICollectionLayoutListConfiguration = ObjCClass(
  'UICollectionLayoutListConfiguration')
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')


class MainViewController(UIViewController):

  modernCollectionView: UICollectionView = objc_property()

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'- {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    #print(f'\t{NSStringFromClass(__class__)}: loadView')

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    #print(f'\t{NSStringFromClass(__class__)}: viewDidLoad')

    # --- Navigation
    self.navigationItem.title = NSStringFromClass(__class__) if (
      title := self.navigationItem.title) is None else title

    # --- UICollectionView setup
    appearance = UICollectionLayoutListAppearance.plain
    configuration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(appearance)
    layout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      configuration)

    rectZero = CGRectMake(0.0, 0.0, 0.0, 0.0)
    modernCollectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(rectZero, layout)
    modernCollectionView.backgroundColor = UIColor.systemDarkPurpleColor()

    # --- Layout
    self.view.addSubview_(modernCollectionView)
    modernCollectionView.translatesAutoresizingMaskIntoConstraints = False

    layoutMarginsGuide = self.view.layoutMarginsGuide
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    NSLayoutConstraint.activateConstraints_([
      modernCollectionView.centerXAnchor.constraintEqualToAnchor_(
        layoutMarginsGuide.centerXAnchor),
      modernCollectionView.centerYAnchor.constraintEqualToAnchor_(
        layoutMarginsGuide.centerYAnchor),
      modernCollectionView.widthAnchor.constraintEqualToAnchor_multiplier_(
        layoutMarginsGuide.widthAnchor, 0.8),
      modernCollectionView.heightAnchor.constraintEqualToAnchor_multiplier_(
        layoutMarginsGuide.heightAnchor, 0.8),
    ])
    self.modernCollectionView = modernCollectionView

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewWillAppear_')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewDidAppear_')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    # print(f'\t{NSStringFromClass(__class__)}: viewWillDisappear_')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'\t{NSStringFromClass(__class__)}: viewDidDisappear_')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'{__class__}: didReceiveMemoryWarning')


if __name__ == '__main__':
  from rbedge.app import App
  from rbedge.enumerations import UIModalPresentationStyle

  main_vc = MainViewController.new()

  #presentation_style = UIModalPresentationStyle.fullScreen
  presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()

