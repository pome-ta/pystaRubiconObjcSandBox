import ctypes
from enum import Enum, auto

from pyrubicon.objc.api import Block, ObjCClass, ObjCInstance, ObjCProtocol, objc_method, objc_property, NSString
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
UICollectionViewCellRegistration = ObjCClass(
  'UICollectionViewCellRegistration')
UICollectionViewListCell = ObjCClass('UICollectionViewListCell')
NSDiffableDataSourceSnapshot = ObjCClass('NSDiffableDataSourceSnapshot')

UICollectionViewDelegate = ObjCProtocol('UICollectionViewDelegate')
# ---

# [モダンなUICollectionViewでシンプルなリストレイアウト その1 〜 概要](https://zenn.dev/samekard_dev/articles/43991e9321b6c9)


class Section(Enum):
  main = auto()


prefectures = ['福岡', '佐賀', '長崎', '大分', '熊本', '宮崎', '鹿児島']


class ViewController(UIViewController, protocols=[
    UICollectionViewDelegate,
]):

  
  collectionView: UICollectionView = objc_property()
  #sdataSource: UICollectionViewDiffableDataSource = objc_property()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title
    self.view.backgroundColor = UIColor.systemDarkRedColor()

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
    #section.contentInsets = NSDirectionalEdgeInsetsMake(10.0, 10.0, 10.0, 10.0)

    layout = UICollectionViewCompositionalLayout.alloc().initWithSection_(
      section)

    self.collectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(self.view.bounds, layout)
    self.collectionView.backgroundColor = UIColor.systemDarkPurpleColor()

    autoresizingMask = UIViewAutoresizing.flexibleHeight | UIViewAutoresizing.flexibleWidth
    self.collectionView.autoresizingMask = autoresizingMask
    self.view.addSubview_(self.collectionView)
    self.collectionView.delegate = self

    @Block
    def configurationHandler(cell: objc_id, indexPath: objc_id,
                             identifier: objc_id) -> None:
      print('j')
      contentConfiguration = cell.defaultContentConfiguration()
      contentConfiguration.text = str(identifier)
      cell.contentConfiguration = contentConfiguration

    cellRegistration = UICollectionViewCellRegistration.registrationWithCellClass_configurationHandler_(
      UICollectionViewListCell, configurationHandler)

    @Block
    def cellProvider(collectionView: objc_id, indexPath: objc_id,
                     identifier: objc_id) -> objc_id:
      print('h')
      return collectionView.dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_(
        cellRegistration, indexPath, identifier).ptr

    dataSource = UICollectionViewDiffableDataSource.alloc().initWithCollectionView_cellProvider_(self.collectionView, cellProvider)
    #self.collectionView.dataSource = UICollectionViewDiffableDataSource.alloc().initWithCollectionView_cellProvider_(self.collectionView, cellProvider)

    #dataSource = UICollectionViewDiffableDataSource.new()
    #pdbr.state(dataSource)
    #print(dataSource)

    snapshot = NSDiffableDataSourceSnapshot.alloc().init()
    #snapshot = NSDiffableDataSourceSnapshot.new()
    snapshot.appendSectionsWithIdentifiers_([Section.main])
    #snapshot.appendSectionsWithIdentifiers_([0])
    snapshot.appendItemsWithIdentifiers_intoSectionWithIdentifier_(prefectures, Section.main)
    #snapshot.appendItemsWithIdentifiers_intoSectionWithIdentifier_(prefectures, 0)
    #pdbr.state(snapshot)
    #print(dir(snapshot))
    #print(snapshot)
    #print(snapshot.impl)
    #self.collectionView.dataSource.applySnapshot_animatingDifferences_(snapshot, False)
    #dataSource.applySnapshot_animatingDifferences_(snapshot, False)
    #self.dataSource.applySnapshot_animatingDifferences_(snapshot, False)
    #print(dataSource)
    #pdbr.state(self.collectionView)
    pdbr.state(self)

  @objc_method
  def collectionView_didSelectItemAtIndexPath_(self, collectionView,
                                               indexPath):
    pdbr.state(collectionView)


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  main_vc = ViewController.new()

  present_viewController(main_vc)

