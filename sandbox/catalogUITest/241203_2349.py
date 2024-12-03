'''
  note: `UICollectionViewController`
'''
import ctypes
from pyrubicon.objc.api import ObjCClass, ObjCProtocol, ObjCInstance, Block
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from rbedge.functions import NSStringFromClass
from rbedge import pdbr

from rbedge.enumerations import (
  UICollectionLayoutListAppearance, )

UICollectionViewController = ObjCClass('UICollectionViewController')
UICollectionViewDataSource = ObjCProtocol('UICollectionViewDataSource')
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

class CollectionViewController(UICollectionViewController,
                               protocols=[
                                 UICollectionViewDataSource,
                                 UICollectionViewDelegate,
                               ]):



#class CollectionViewController(UICollectionViewController):
  #cellreg: UICollectionViewCellRegistration = objc_property()
  #datasource: UICollectionViewDiffableDataSource = objc_property(weak=True)
  #datasource: UICollectionViewDiffableDataSource = objc_property()
  #snap = objc_property()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title
    #self.collectionView.dataSource = self
    #self.dataSource = self
    #self.delegate = self
    # --- View
    
  @objc_method  # private
  def configureDataSource(self):

    @Block
    def configurationHandler(_cell: objc_id, _indexPath: objc_id,
                             _item: objc_id) -> None:
      cell = ObjCInstance(_cell)
      indexPath = ObjCInstance(_indexPath)
      item = ObjCInstance(_item)

    cellRegistration = UICollectionViewCellRegistration.registrationWithCellClass_configurationHandler_(
      UICollectionViewListCell, configurationHandler)

    @Block
    def cellProvider(_collectionView: objc_id, _indexPath: objc_id,
                     _item: objc_id) -> ObjCInstance:
      collectionView = ObjCInstance(_collectionView)
      indexPath = ObjCInstance(_indexPath)
      item = ObjCInstance(_item)
      return collectionView.dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_(cellRegistration, indexPath, item)

    self.dataSource = UICollectionViewDiffableDataSource.alloc(
    ).initWithCollectionView_cellProvider_(self.collectionView, cellProvider)

    self.pep = ['manny', 'moe', 'jack']

    snapshot = NSDiffableDataSourceSnapshot.alloc().init()
    snapshot.appendSectionsWithIdentifiers_([0])
    snapshot.appendItemsWithIdentifiers_(at(self.pep))
    #snapshot.appendItemsWithIdentifiers_([])
    self.dataSource.applySnapshot_animatingDifferences_(snapshot, False)
    #pdbr.state(dataSource)
    

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    pdbr.state(self.collectionView)
    #self.datasource.applySnapshot_animatingDifferences_(self.snap, False)

  '''
  @objc_method
  def collectionView_numberOfItemsInSection_(self, collectionView,
                                             section: int) -> int:

    return 3

  @objc_method
  def collectionView_cellForItemAtIndexPath_(self, collectionView,
                                             indexPath) -> objc_id:
    return collectionView.dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_(
      self.cellreg, indexPath, self.pep[indexPath.item])
  '''


if __name__ == '__main__':
  from rbedge import present_viewController
  from rbedge.enumerations import UIModalPresentationStyle

  _appearance = UICollectionLayoutListAppearance.sidebar
  #_appearance = UICollectionLayoutListAppearance.plain
  listConfiguration = UICollectionLayoutListConfiguration.alloc(
  ).initWithAppearance_(_appearance)

  layout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
    listConfiguration)

  vc = CollectionViewController.alloc().initWithCollectionViewLayout_(layout)

  style = UIModalPresentationStyle.fullScreen
  #style = UIModalPresentationStyle.pageSheet
  present_viewController(vc, style)

