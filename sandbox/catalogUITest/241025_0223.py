"""
note: 迷走中
ref: [モダンなUICollectionViewでシンプルなリストレイアウト その1 〜 概要](https://zenn.dev/samekard_dev/articles/43991e9321b6c9)
  - Diffable DataSource
"""
import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import objc_method, objc_property, at
from pyrubicon.objc.runtime import send_super, objc_id

#from rbedge.types import NSDirectionalEdgeInsetsMake
from rbedge.enumerations import UIViewAutoresizing
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

UICollectionViewLayout = ObjCClass('UICollectionViewLayout')
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')

UICollectionViewCellRegistration = ObjCClass(
  'UICollectionViewCellRegistration')

# wip: 後ほど独自拡張
UICollectionViewListCell = ObjCClass('UICollectionViewListCell')

NSDiffableDataSourceSnapshot = ObjCClass('NSDiffableDataSourceSnapshot')

NSUUID = ObjCClass('NSUUID')

prefectures = [
  '福岡',
  '佐賀',
  '長崎',
  '大分',
  '熊本',
  '宮崎',
  '鹿児島',
]


class ViewController(UIViewController):

  collectionView: UICollectionView = objc_property()
  dataSource: UICollectionViewDiffableDataSource = objc_property()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    # --- Navigation
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    # xxx: 先に宣言してみる
    #self.collectionView = UICollectionView.alloc()

    self.configureHierarchy()
    self.configureDataSource()

  @objc_method
  def viewDidAppear_(self, animated: bool):
    # xxx: 引数不要?
    send_super(__class__, self, 'viewDidAppear:')
    print('viewDidAppear')
    #pdbr.state(self.collectionView)
    print(self.collectionView)

  @objc_method
  def createLayout(self) -> ctypes.py_object:
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

    # wip: `NSDirectionalEdgeInsetsMake`
    #section.setContentInsets_()
    #m = NSDirectionalEdgeInsetsMake(10.0, 10.0, 10.0, 10.0)

    layout = UICollectionViewCompositionalLayout.alloc().initWithSection_(
      section)
    return layout

  @objc_method
  def configureHierarchy(self):
    view = self.view

    #self.collectionView.initWithFrame_collectionViewLayout_(view.bounds, self.createLayout())
    self.collectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(view.bounds, self.createLayout())

    #self.collectionView.autoresizingMask = UIViewAutoresizing.flexibleHeight | UIViewAutoresizing.flexibleWidth

    self.collectionView.setAutoresizingMask_(
      UIViewAutoresizing.flexibleHeight | UIViewAutoresizing.flexibleWidth)
    view.addSubview_(self.collectionView)
    # wip: `collectionView.delegate = self //タップ操作へ対応するため`

  @objc_method
  def configureDataSource(self):
    print('configureDataSource')

    @Block
    def configurationHandler(_cell: objc_id, _indexPath: objc_id,
                             _item: objc_id) -> None:
      print('Block: configurationHandler')

      cell = ObjCInstance(_cell)
      indexPath = ObjCInstance(_indexPath)
      item = ObjCInstance(_item)
      # wip: 後ほど独自拡張
      configuration = cell.defaultContentConfiguration()
      configuration.setText_('hoge')
      cell.setContentConfiguration_(configuration)

    @Block
    def cellProvider(_collectionView: objc_id, _indexPath: objc_id,
                     _item: objc_id) -> ctypes.py_object:
      print('Block: cellProvider')
      collectionView = ObjCInstance(_collectionView)
      indexPath = ObjCInstance(_indexPath)
      item = ObjCInstance(_item)

      return collectionView.dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_(
        cellRegistration, indexPath, item)

    cellRegistration = UICollectionViewCellRegistration.registrationWithCellClass_configurationHandler_(
      UICollectionViewListCell, configurationHandler)

    pdbr.state(cellRegistration)

    dataSource = UICollectionViewDiffableDataSource.alloc(
    ).initWithCollectionView_cellProvider_(self.collectionView, cellProvider)

    snapshot = NSDiffableDataSourceSnapshot.alloc().init()
    snapshot.appendSectionsWithIdentifiers_(at([0]))
    snapshot.appendItemsWithIdentifiers_intoSectionWithIdentifier_(
      at([
        NSUUID.UUID(),
        NSUUID.UUID(),
        #prefectures
      ]),
      0)

    #snapshot.appendItemsWithIdentifiers_intoSectionWithIdentifier_(prefectures, 0)
    self.dataSource = dataSource
    #self.dataSource.applySnapshot_animatingDifferences_(snapshot, True)

    #print(self.dataSource)
    #print(dataSource)
    #self.collectionView.setDataSource_(dataSource)
    #pdbr.state(snapshot)
    #pdbr.state(dataSource)


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  vc = ViewController.new()
  style = UIModalPresentationStyle.fullScreen
  present_viewController(vc, style)
  #print(CGRectZero)

