"""
note: 迷走中
ref: [モダンなUICollectionViewでシンプルなリストレイアウト その1 〜 概要](https://zenn.dev/samekard_dev/articles/43991e9321b6c9)
  - Diffable DataSource


"""
from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import objc_method, objc_property, at
from pyrubicon.objc.runtime import send_super, objc_id

#from rbedge.types import NSDirectionalEdgeInsetsMake
from rbedge.enumerations import UICollectionLayoutListAppearance, UIViewAutoresizing

from rbedge.functions import NSStringFromClass

UIViewController = ObjCClass('UIViewController')
UICollectionView = ObjCClass('UICollectionView')
UICollectionViewDiffableDataSource = ObjCClass(
  'UICollectionViewDiffableDataSource')

NSCollectionLayoutSize = ObjCClass('NSCollectionLayoutSize')
NSCollectionLayoutDimension = ObjCClass('NSCollectionLayoutDimension')
NSCollectionLayoutItem = ObjCClass('NSCollectionLayoutItem')
NSCollectionLayoutGroup = ObjCClass('NSCollectionLayoutGroup')
NSCollectionLayoutSection = ObjCClass('NSCollectionLayoutSection')


class ViewController(UIViewController):

  dataSource: UICollectionViewDiffableDataSource = objc_property(weak=True)
  collectionView: UICollectionView = objc_property(weak=True)

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    # --- Navigation
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    self.configureHierarchy()

  @objc_method
  def viewDidAppear_(self, animated: bool):
    # xxx: 引数不要?
    send_super(__class__, self, 'viewDidAppear:')
    #print('viewDidAppear')

  @objc_method
  def createLayout(self):
    itemSize = NSCollectionLayoutSize.sizeWithWidthDimension_heightDimension_(
      NSCollectionLayoutDimension.fractionalWidthDimension_(1.0),
      NSCollectionLayoutDimension.fractionalHeightDimension_(1.0))
    item = NSCollectionLayoutItem.itemWithLayoutSize_(itemSize)
    groupSize = NSCollectionLayoutSize.sizeWithWidthDimension_heightDimension_(
      NSCollectionLayoutDimension.fractionalWidthDimension_(1.0),
      NSCollectionLayoutDimension.absoluteDimension_(44.0))
    group = NSCollectionLayoutGroup.horizontalGroupWithLayoutSize_subitems_(
      groupSize, at([
        item,
      ]))
    section = NSCollectionLayoutSection.sectionWithGroup_(group)
    section.setInterGroupSpacing_(0)
    
    #section.setContentInsets_()
    #m = NSDirectionalEdgeInsetsMake(10.0, 10.0, 10.0, 10.0)
    
    pdbr.state(m)

  @objc_method
  def configureHierarchy(self):
    #print('configureHierarchy')
    self.createLayout()


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  vc = ViewController.new()
  style = UIModalPresentationStyle.fullScreen
  present_viewController(vc, style)
  #print(CGRectZero)

