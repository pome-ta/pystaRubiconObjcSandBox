'''
  note:
    - [モダンなUICollectionViewでシンプルなリストレイアウト その1 〜 概要](https://zenn.dev/samekard_dev/articles/43991e9321b6c9)
    - [PythonistaでRubicon-ObjCを使う](https://zenn.dev/qqfunc/articles/b39a657990c9f0)
'''

import ctypes

import objc_util

from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id,objc_block

from rbedge.types import NSDirectionalEdgeInsetsMake

from rbedge import pdbr

ObjCClass.auto_rename = True

NSOperation = ObjCClass('NSOperation')
NSOperationQueue = ObjCClass('NSOperationQueue')
UIApplication = ObjCClass('UIApplication')
UIColor = ObjCClass('UIColor')
UIViewController = ObjCClass('UIViewController')

NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

UICollectionView = ObjCClass('UICollectionView')
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')
UICollectionViewCellRegistration = ObjCClass(
  'UICollectionViewCellRegistration')
UICollectionViewListCell = ObjCClass('UICollectionViewListCell')
UICollectionViewCell = ObjCClass('UICollectionViewCell')

UICollectionViewDiffableDataSource = ObjCClass(
  'UICollectionViewDiffableDataSource')
NSDiffableDataSourceSnapshot = ObjCClass('NSDiffableDataSourceSnapshot')

NSCollectionLayoutSize = ObjCClass('NSCollectionLayoutSize')
NSCollectionLayoutDimension = ObjCClass('NSCollectionLayoutDimension')
NSCollectionLayoutItem = ObjCClass('NSCollectionLayoutItem')
NSCollectionLayoutGroup = ObjCClass('NSCollectionLayoutGroup')
NSCollectionLayoutSection = ObjCClass('NSCollectionLayoutSection')

NSUUID = ObjCClass('NSUUID')

class ViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.view.backgroundColor = UIColor.blueColor
    self.configureHierarchy()
    self.configureDataSource()
    #print('Viewが読み込まれました')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print('viewDidAppear_')
    #pdbr.state(self.collectionView)
    self.initDataSource()

  @objc_method
  def configureHierarchy(self):
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

    collectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(self.view.bounds, layout)
    self.view.addSubview_(collectionView)

    # --- Layout
    collectionView.translatesAutoresizingMaskIntoConstraints = False
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide
    NSLayoutConstraint.activateConstraints_([
      collectionView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      collectionView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      collectionView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor, 1.0),
      collectionView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor, 1.0),
    ])
    #collectionView.delegate = self
    self.collectionView = collectionView

    #pdbr.state(collectionView)

  @objc_method
  def configureDataSource(self):

    @Block
    def configurationHandler(_cell: objc_id, _indexPath: objc_id,
                             _item: objc_id) -> objc_block:
      cell = ObjCInstance(_cell)

    cellRegistration = UICollectionViewCellRegistration.registrationWithCellClass_configurationHandler_(
      UICollectionViewListCell, configurationHandler)

    @Block
    def cellProvider(_collectionView: objc_id, _indexPath: objc_id,
                     _item: objc_id) -> objc_id:
      collectionView = ObjCInstance(_collectionView)

      indexPath = ObjCInstance(_indexPath)
      item = ObjCInstance(_item)
      return collectionView.dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_(
        cellRegistration, indexPath, item)

    self.dataSource = UICollectionViewDiffableDataSource.alloc(
    ).initWithCollectionView_cellProvider_(self.collectionView, cellProvider)


  @objc_method
  def initDataSource(self):
    

    #pdbr.state(self.collectionView)
    snapshot = NSDiffableDataSourceSnapshot.alloc().init()
    snapshot.appendSectionsWithIdentifiers_([0])

    snapshot.appendItemsWithIdentifiers_intoSectionWithIdentifier_(
      [NSUUID.UUID(), NSUUID.UUID()], 0)
    #snapshot.appendItemsWithIdentifiers_([NSUUID.UUID(),NSUUID.UUID()])
    #self.dataSource.applySnapshot_animatingDifferences_(snapshot, False)
    
    #pdbr.state(snapshot)
    #pdbr.state()
    pdbr.state(self.dataSource)
    #self.dataSource.applySnapshot_animatingDifferences_(snapshot, True)
    @objc_util.on_main_thread
    def thread():
      self.dataSource.applySnapshot_animatingDifferences_(snapshot, False)
    #thread()


class MainOperation(NSOperation):

  @objc_method
  def main(self):
    send_super(__class__, self, 'main')
    app = UIApplication.sharedApplication
    rootVC = app.keyWindow.rootViewController
    while childVC := rootVC.presentedViewController:
      rootVC = childVC
    mainVC = ViewController.new().autorelease()
    rootVC.presentViewController(mainVC, animated=True, completion=None)


if __name__ == "__main__":
  operation = MainOperation.new()
  queue = NSOperationQueue.mainQueue
  queue.addOperation(operation)
  queue.waitUntilAllOperationsAreFinished()


