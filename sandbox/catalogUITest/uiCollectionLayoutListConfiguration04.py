import ctypes

from pyrubicon.objc.api import Block, ObjCClass, ObjCProtocol, objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import NSInteger

from rbedge.enumerations import (
  UICollectionLayoutListAppearance,
  UICollectionLayoutListHeaderMode,
  UIViewAutoresizing,
)
from rbedge.functions import NSStringFromClass

#ObjCClass.auto_rename = True

UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- UICollectionView
UICollectionView = ObjCClass('UICollectionView')
UICollectionViewDiffableDataSource = ObjCClass(
  'UICollectionViewDiffableDataSource')
NSCollectionLayoutSize = ObjCClass('NSCollectionLayoutSize')
NSCollectionLayoutDimension = ObjCClass('NSCollectionLayoutDimension')
NSCollectionLayoutItem = ObjCClass('NSCollectionLayoutItem')
NSCollectionLayoutGroup = ObjCClass('NSCollectionLayoutGroup')
NSCollectionLayoutSection = ObjCClass('NSCollectionLayoutSection')

# ---

UICollectionViewCellRegistration = ObjCClass(
  'UICollectionViewCellRegistration')

UICollectionViewListCell = ObjCClass('UICollectionViewListCell')
#UICollectionViewLayout = ObjCClass('UICollectionViewLayout')  # todo: 型呼び出し
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')
UICollectionLayoutListConfiguration = ObjCClass(
  'UICollectionLayoutListConfiguration')

UICollectionViewDataSource = ObjCProtocol('UICollectionViewDataSource')
UICollectionViewDelegate = ObjCProtocol('UICollectionViewDelegate')

# [モダンなUICollectionViewでシンプルなリストレイアウト その1 〜 概要](https://zenn.dev/samekard_dev/articles/43991e9321b6c9)

prefectures = ['福岡', '佐賀', '長崎', '大分', '熊本', '宮崎', '鹿児島']


class ViewController(UIViewController):
  dataSource: UICollectionViewDiffableDataSource = objc_property()
  collectionView: UICollectionView = objc_property()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title
    self.view.backgroundColor = UIColor.systemDarkRedColor()

    #pdbr.state(NSCollectionLayoutDimension)
    #pdbr.state(NSCollectionLayoutSize)

    itemSize = NSCollectionLayoutSize.sizeWithWidthDimension_heightDimension_(
      NSCollectionLayoutDimension.fractionalWidthDimension_(1.0),
      NSCollectionLayoutDimension.fractionalHeightDimension_(1.0))

    item = NSCollectionLayoutItem.itemWithLayoutSize_(itemSize)

    groupSize = NSCollectionLayoutSize.sizeWithWidthDimension_heightDimension_(
      NSCollectionLayoutDimension.fractionalWidthDimension_(1.0),
      NSCollectionLayoutDimension.absoluteDimension_(44))

    group = NSCollectionLayoutGroup.horizontalGroupWithLayoutSize_subitems_(
      groupSize, [
        item,
      ])

    section = NSCollectionLayoutSection.sectionWithGroup_(group)
    section.interGroupSpacing=0
    pdbr.state(section)

  # --- extension
  @objc_method
  def createLayout(self):
    #sizeWithWidthDimension_heightDimension_

    return None


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  main_vc = ViewController.new()

  present_viewController(main_vc)

