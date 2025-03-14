'''
  todo: 再度シンプルチャレンジ
    - [Collection View Content Configuration in iOS 14 - BiTE Interactive](https://www.biteinteractive.com/collection-view-content-configuration-in-ios-14/)
'''
import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance, ObjCProtocol, Block
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGRectMake

from rbedge.functions import NSStringFromClass
from rbedge import pdbr

from rbedge.enumerations import (
  UICollectionLayoutListAppearance, )

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

UIColor = ObjCClass('UIColor')

UICollectionView = ObjCClass('UICollectionView')
UICollectionViewDataSource = ObjCProtocol('UICollectionViewDataSource')
UICollectionLayoutListConfiguration = ObjCClass(
  'UICollectionLayoutListConfiguration')
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')
UICollectionViewDiffableDataSource = ObjCClass(
  'UICollectionViewDiffableDataSource')
UICollectionViewCellRegistration = ObjCClass(
  'UICollectionViewCellRegistration')
UICollectionViewListCell = ObjCClass('UICollectionViewListCell')


class CollectionViewController(UIViewController,
                               protocols=[
                                 UICollectionViewDataSource,
                               ]):

  #class CollectionViewController(UIViewController):
  collectionView: UICollectionView = objc_property()
  cellreg: UICollectionViewCellRegistration = objc_property()

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    cg_zero = CGRectMake(0.0, 0.0, 0.0, 0.0)
    self.collectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(cg_zero, self.generateLayout())
    self.collectionView.dataSource = self
    return self

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    # --- View
    self.view.backgroundColor = UIColor.systemBrownColor()  # todo: 確認用
    self.view.addSubview_(self.collectionView)

    # --- Layout
    self.collectionView.translatesAutoresizingMaskIntoConstraints = False
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide
    NSLayoutConstraint.activateConstraints_([
      self.collectionView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      self.collectionView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      self.collectionView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor, 1.0),
      self.collectionView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor, 1.0),
    ])

    @Block
    def cellProvider(_cell: objc_id, _indexPath: objc_id,
                     _item: objc_id) -> None:
      #pdbr.state(_cell)
      cell = ObjCInstance(_cell)
      indexPath = ObjCInstance(_indexPath)
      item = ObjCInstance(_item)
      pdbr.state(ObjCInstance(_indexPath))
      config = cell.defaultContentConfiguration()
      config.setText_(item)
      cell.setContentConfiguration_(config)

    #pdbr.state(UICollectionViewDiffableDataSource.alloc())
    #initWithCollectionView_cellProvider_

    self.cellreg = UICollectionViewCellRegistration.registrationWithCellClass_configurationHandler_(
      UICollectionViewListCell, cellProvider)

    self.pep = ["manny", "moe", "jack"]
    #self.datasource = UICollectionViewDiffableDataSource.alloc( ).initWithCollectionView_cellProvider_(self.collectionView, cellreg)
    #snapshot = self.datasource.snapshot()
    #pdbr.state(self.datasource)
    #pdbr.state(cellreg)

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #pdbr.state(self.collectionView)
    #pdbr.state(self.cellreg)
    #print(self.pep)

  @objc_method
  def collectionView_numberOfItemsInSection_(self, collectionView,
                                             section: int) -> int:

    return 3

  @objc_method
  def collectionView_cellForItemAtIndexPath_(self, collectionView,
                                             indexPath) -> objc_id:
    return collectionView.dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_(
      self.cellreg, indexPath, self.pep[indexPath.item])

  # --- private
  @objc_method
  def generateLayout(self) -> ObjCInstance:
    _appearance = UICollectionLayoutListAppearance.sidebar
    #_appearance = UICollectionLayoutListAppearance.plain
    listConfiguration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(_appearance)

    layout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      listConfiguration)
    #pdbr.state(listConfiguration.appearance)
    #print(listConfiguration.appearance)
    return layout


if __name__ == '__main__':
  from rbedge import present_viewController
  from rbedge.enumerations import UIModalPresentationStyle

  vc = CollectionViewController.new()

  style = UIModalPresentationStyle.fullScreen
  #style = UIModalPresentationStyle.pageSheet
  present_viewController(vc, style)

