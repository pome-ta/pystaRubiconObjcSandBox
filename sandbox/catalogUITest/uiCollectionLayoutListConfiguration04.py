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
from rbedge.types import NSDirectionalEdgeInsetsMake

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
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')

# ---

UICollectionViewCellRegistration = ObjCClass(
  'UICollectionViewCellRegistration')

UICollectionViewListCell = ObjCClass('UICollectionViewListCell')
#UICollectionViewLayout = ObjCClass('UICollectionViewLayout')  # todo: 型呼び出し

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

    self.configureHierarchy()
    #self.createLayout()
    

  # --- extension
  @objc_method
  def createLayout(self)->ctypes.c_void_p:
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
    section.interGroupSpacing = 0
    section.contentInsets = NSDirectionalEdgeInsetsMake(10.0, 10.0, 10.0, 10.0)
    
    

    layout = UICollectionViewCompositionalLayout.alloc().initWithSection_(
      section)

    #return layout
    #pdbr.state(layout)
    return layout

  @objc_method
  def configureHierarchy(self):
    self.collectionView = UICollectionView.alloc(
    )  #.initWithFrame_collectionViewLayout_(self.view.bounds, self.createLayout())
    print(self.createLayout())

    #initWithFrame_collectionViewLayout_

    #pdbr.state(self.collectionView)
    #print(self.view.bounds)
    #print(self.createLayout())
    #autoresizingMask = UIViewAutoresizing.flexibleHeight | UIViewAutoresizing.flexibleWidth
    #self.collectionView.autoresizingMask = autoresizingMask
    #self.view.addSubview_(self.collectionView)


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  main_vc = ViewController.new()

  present_viewController(main_vc)

