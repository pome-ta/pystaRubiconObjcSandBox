'''
  note: シンプルに`UICollectionViewDiffableDataSource` のやつやる
    - [UICollectionViewでUITableViewのようなUIを実現する。ただし#available(iOS 14.0, *) #Swift - Qiita](https://qiita.com/sohichiro/items/9a3394551b8d76d2a346)
'''
import ctypes
import functools

from pyrubicon.objc.api import ObjCClass, ObjCInstance, ObjCProtocol, Block
from pyrubicon.objc.api import objc_method, objc_property, objc_block
from pyrubicon.objc.runtime import send_super, objc_id, libobjc

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
NSUUID = ObjCClass('NSUUID')

NSThread = ObjCClass('NSThread')


class struct_dispatch_queue_s(ctypes.Structure):
  pass


_dispatch_main_q = struct_dispatch_queue_s.in_dll(libobjc, '_dispatch_main_q')


def dispatch_get_main_queue():
  return ObjCInstance(ctypes.cast(ctypes.byref(_dispatch_main_q), objc_id))


libobjc.dispatch_async.restype = None
libobjc.dispatch_async.argtypes = (objc_id, objc_block)

#pdbr.state(UICollectionViewListCell.className())





'''
class ViewController(UIViewController, protocols=[
    UICollectionViewDelegate,
]):
'''
class ViewController(UIViewController):
  #collectionView: UICollectionView = objc_property()
  #dataSource: UICollectionViewDiffableDataSource = objc_property()
  snapshot: NSDiffableDataSourceSectionSnapshot = objc_property()
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
    #self.collectionView.reloadData()

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    self.initialSnapshot()
    print('viewWillAppear')
  
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
    
    print('viewDidAppear')
    
  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print('didReceiveMemoryWarning')

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
      #indexPath = ObjCInstance(_indexPath)
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
      return _collectionView.dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_(
        cellRegistration, indexPath, item)

    self.dataSource = UICollectionViewDiffableDataSource.alloc(
    ).initWithCollectionView_cellProvider_(self.collectionView, cellProvider)

    #pdbr.state(self.dataSource)
    #print(self.dataSource.validateIdentifiers())

    #pdbr.state(UICollectionViewDiffableDataSource.new())
    #self.initialSnapshot()
    #pdbr.state(self.collectionView)

  @objc_method  # private
  def generateLayout(self) -> ObjCInstance:
    #_appearance = UICollectionLayoutListAppearance.sidebar
    _appearance = UICollectionLayoutListAppearance.plain
    listConfiguration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(_appearance)
    layout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      listConfiguration)
    return layout

  @objc_method  # private
  def initialSnapshot(self):
    #snapshot = NSDiffableDataSourceSectionSnapshot.alloc().init()
    self.snapshot = NSDiffableDataSourceSnapshot.alloc().init()
    #self.snapshot = self.collectionView.dataSource.snapshot()
    self.snapshot.appendSectionsWithIdentifiers_([0])
    self.snapshot.appendItemsWithIdentifiers_([NSUUID.UUID(), NSUUID.UUID()])
    #pdbr.state(snapshot.sectionIdentifiers.objectAtIndex_(0))
    #pdbr.state(snapshot.validateIdentifiers())
    #snapshot.reloadSectionsWithIdentifiers_([0])
    #snapshot.appendItemsWithIdentifiers_(['a'])
    #snapshot.appendItemsWithIdentifiers_intoSectionWithIdentifier_(['a'], 0)
    #self.snapshot.reloadItemsWithIdentifiers_([''])
    #pdbr.state(self.collectionView.dataSource.snapshot())
    #pdbr.state(self.snapshot)
    #self.collectionView.dataSource.applySnapshot_animatingDifferences_(snapshot, False)
    #self.dataSource.applySnapshotUsingReloadData_(snapshot)
    #self.dataSource.applySnapshot_toSection_animatingDifferences_(snapshot, None, False)
    

    block = Block(
      functools.partial(self.dataSource.applySnapshot_animatingDifferences_,
                        self.snapshot, False), None)
    libobjc.dispatch_async(dispatch_get_main_queue(), block)
    

    #self.dataSource.applySnapshot_animatingDifferences_(snapshot, False)
    #pdbr.state(self.dataSource)
    #print(snapshot)
    #print(self.collectionView.dataSource.snapshot())
    #pdbr.state(snapshot)
    #print(snapshot)
    #pdbr.state(self.collectionView)
    #pdbr.state(self.dataSource)

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

