'''
  note: シンプルに`UICollectionViewDiffableDataSource` のやつやる
    - [UICollectionViewでUITableViewのようなUIを実現する。ただし#available(iOS 14.0, *) #Swift - Qiita](https://qiita.com/sohichiro/items/9a3394551b8d76d2a346)
'''
import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance, ObjCProtocol, Block
from pyrubicon.objc.api import objc_method, objc_property, at
from pyrubicon.objc.runtime import send_super, objc_id

from rbedge.functions import NSStringFromClass
from rbedge import pdbr

from rbedge.enumerations import (
  UICollectionLayoutListAppearance, )

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- CollectionView
UICollectionView = ObjCClass('UICollectionView')
UICollectionViewDelegate = ObjCProtocol('UICollectionViewDelegate')
UICollectionLayoutListConfiguration = ObjCClass(
  'UICollectionLayoutListConfiguration')
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')
UICollectionViewCellRegistration = ObjCClass(
  'UICollectionViewCellRegistration')
UICollectionViewListCell = ObjCClass('UICollectionViewListCell')
UICollectionViewDiffableDataSource = ObjCClass(
  'UICollectionViewDiffableDataSource')
NSDiffableDataSourceSnapshot = ObjCClass('NSDiffableDataSourceSnapshot')
NSDiffableDataSourceSectionSnapshot = ObjCClass(
  'NSDiffableDataSourceSectionSnapshot')
# --- others
UIColor = ObjCClass('UIColor')
'''
class ViewController(UIViewController, protocols=[
    UICollectionViewDelegate,
]):
'''


class ViewController(UIViewController):
  #collectionView: UICollectionView = objc_property()
  #dataSource: UICollectionViewDiffableDataSource = objc_property()
  #snapshot: NSDiffableDataSourceSectionSnapshot = objc_property()
  #cellRegistration=objc_property()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    # --- Navigation
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    # --- View
    self.view.backgroundColor = UIColor.systemDarkRedColor()  # todo: 確認用

    self.configureCollectionView()
    self.configureDataSource()

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(self.collectionView)
    #pdbr.state(self)
    #self.upDateSnapshot()
    #print(self.collectionView)
    #pdbr.state(self.collectionView.dataSource)

  @objc_method  # private
  def configureCollectionView(self):

    collectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(self.view.bounds,
                                          self.generateLayout())
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

  @objc_method  # private
  def configureDataSource(self):

    @Block
    def configurationHandler(_cell: objc_id, _indexPath: objc_id,
                             _item: objc_id) -> None:
      cell = ObjCInstance(_cell)
      indexPath = ObjCInstance(_indexPath)
      item = ObjCInstance(_item)

      config = cell.defaultContentConfiguration()
      config.setText_(item)
      cell.setContentConfiguration_(config)

    cellRegistration = UICollectionViewCellRegistration.registrationWithCellClass_configurationHandler_(
      UICollectionViewListCell, configurationHandler)

    @Block
    def cellProvider(_collectionView: objc_id, _indexPath: objc_id,
                     _item: objc_id) -> objc_id:
      collectionView = ObjCInstance(_collectionView)
      
      indexPath = ObjCInstance(_indexPath)
      item = ObjCInstance(_item)
      return collectionView.dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_(
        cellRegistration, _indexPath, item)

    self.dataSource = UICollectionViewDiffableDataSource.alloc(
    ).initWithCollectionView_cellProvider_(self.collectionView, cellProvider)

    #pdbr.state(UICollectionViewDiffableDataSource.new())
    self.initialSnapshot()

  @objc_method  # private
  def generateLayout(self) -> ObjCInstance:
    _appearance = UICollectionLayoutListAppearance.sidebar
    listConfiguration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(_appearance)
    layout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      listConfiguration)
    return layout

  @objc_method  # private
  def initialSnapshot(self) -> ObjCInstance:
    #snapshot = NSDiffableDataSourceSectionSnapshot.alloc().init()
    snapshot = NSDiffableDataSourceSnapshot.alloc().init()
    #self.snapshot = self.collectionView.dataSource.snapshot()
    snapshot.appendSectionsWithIdentifiers_([0])
    #snapshot.reloadSectionsWithIdentifiers_([0])
    #snapshot.appendItemsWithIdentifiers_(['a'])
    #snapshot.appendItemsWithIdentifiers_intoSectionWithIdentifier_(['a'], 0)
    #self.snapshot.reloadItemsWithIdentifiers_([''])
    #pdbr.state(self.collectionView.dataSource.snapshot())
    #pdbr.state(self.snapshot)
    #self.collectionView.dataSource.applySnapshot_animatingDifferences_(snapshot, False)
    self.dataSource.applySnapshot_animatingDifferences_(snapshot, False)
    #print(snapshot)
    #print(self.collectionView.dataSource.snapshot())
    #pdbr.state(snapshot)
    #print(snapshot)
    pdbr.state(self.collectionView)

  @objc_method  # private
  def upDateSnapshot(self) -> ObjCInstance:
    #snapshot = NSDiffableDataSourceSectionSnapshot.alloc().init()
    #snapshot = NSDiffableDataSourceSnapshot.alloc().init()
    snapshot = self.collectionView.dataSource.snapshot()
    snapshot.appendSectionsWithIdentifiers_([1])
    #snapshot.reloadSectionsWithIdentifiers_([0])
    #snapshot.appendItemsWithIdentifiers_([])
    #self.snapshot.reloadItemsWithIdentifiers_([''])
    #pdbr.state(self.collectionView.dataSource.snapshot())
    #pdbr.state(self.snapshot)
    #self.dataSource.applySnapshot_animatingDifferences_(snapshot, False)
    #print(snapshot)


if __name__ == '__main__':
  from rbedge import present_viewController
  from rbedge.enumerations import UIModalPresentationStyle

  vc = ViewController.new()

  style = UIModalPresentationStyle.fullScreen
  #style = UIModalPresentationStyle.pageSheet
  present_viewController(vc, style)

