import ctypes
from enum import Enum, auto

from pyrubicon.objc.api import Block, ObjCClass, ObjCInstance, ObjCProtocol, objc_method, objc_property, NSString
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import NSInteger

from rbedge.enumerations import UIViewAutoresizing

from rbedge.functions import NSStringFromClass
from rbedge.types import NSDirectionalEdgeInsetsMake

#ObjCClass.auto_rename = True

UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- UICollectionView
UICollectionView = ObjCClass('UICollectionView')
NSCollectionLayoutSize = ObjCClass('NSCollectionLayoutSize')
NSCollectionLayoutDimension = ObjCClass('NSCollectionLayoutDimension')

# ---
from pyrubicon.objc.runtime import load_library
from pyrubicon.objc.types import CGRect

from rbedge.enumerations import (
  UICollectionLayoutListAppearance,
  UICollectionLayoutListHeaderMode,
)

UICollectionViewLayout = ObjCClass('UICollectionViewLayout')

UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')
UICollectionLayoutListConfiguration = ObjCClass(
  'UICollectionLayoutListConfiguration')

CoreGraphics = load_library('CoreGraphics')
CGRectZero = CGRect.in_dll(CoreGraphics, 'CGRectZero')

# [モダンなUICollectionViewでシンプルなリストレイアウト その1 〜 概要](https://zenn.dev/samekard_dev/articles/43991e9321b6c9)


class Section(Enum):
  main = auto()


prefectures = ['福岡', '佐賀', '長崎', '大分', '熊本', '宮崎', '鹿児島']


class ViewController(UIViewController):

  collectionView: UICollectionView = objc_property()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title
    self.view.backgroundColor = UIColor.systemDarkRedColor()

    self.configureHierarchy()

  @objc_method
  def createLayout(self) -> ObjCInstance:  # -> UICollectionViewLayout
    dimension = NSCollectionLayoutDimension

    listConfiguration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(UICollectionLayoutListAppearance.plain)
    listConfiguration.headerMode = UICollectionLayoutListHeaderMode.firstItemInSection

    return UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      listConfiguration)

  @objc_method
  def configureHierarchy(self):
    self.collectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(self.view.bounds,
                                          self.createLayout())

    self.collectionView.backgroundColor = UIColor.systemDarkPurpleColor()

    autoresizingMask = UIViewAutoresizing.flexibleHeight | UIViewAutoresizing.flexibleWidth
    self.collectionView.autoresizingMask = autoresizingMask
    self.view.addSubview_(self.collectionView)
    #pdbr.state(self.collectionView)


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  main_vc = ViewController.new()

  present_viewController(main_vc)

