"""
  note: [UICollectionViewでUITableViewのようなUIを実現する。ただし#available(iOS 14.0, *) #Swift - Qiita](https://qiita.com/sohichiro/items/9a3394551b8d76d2a346)
"""

import ctypes

from pyrubicon.objc.api import ObjCClass, Block
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGRectMake

from rbedge.enumerations import (
  UICollectionLayoutListAppearance, )

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
UIColor = ObjCClass('UIColor')

UICollectionView = ObjCClass('UICollectionView')
UICollectionLayoutListConfiguration = ObjCClass(
  'UICollectionLayoutListConfiguration')
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')
UICollectionViewDiffableDataSource = ObjCClass(
  'UICollectionViewDiffableDataSource')
UICollectionViewCellRegistration = ObjCClass(
  'UICollectionViewCellRegistration')
UICollectionViewListCell = ObjCClass('UICollectionViewListCell')
NSDiffableDataSourceSnapshot = ObjCClass('NSDiffableDataSourceSnapshot')


class ModernCollectionViewViewController(UIViewController):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print('\tdealloc')
    pass

  # MARK: - View Life Cycle
  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    # xxx: `collectionView` での関数名衝突回避
    modernCollectionView = UICollectionView.alloc()

    self.configureLayout_(modernCollectionView)
    modernDataSource = self.configureCellRegistration_(modernCollectionView)

    self.modernCollectionView = modernCollectionView
    self.modernDataSource = modernDataSource

  @objc_method  # --- private
  def configureLayout_(self, collectionView):
    _appearance = UICollectionLayoutListAppearance.plain
    configuration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(_appearance)
    layout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      configuration)
    collectionView.initWithFrame_collectionViewLayout_(
      CGRectMake(0.0, 0.0, 0.0, 0.0), layout)
    collectionView.backgroundColor = UIColor.systemDarkPurpleColor()

    # --- Layout
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    self.view.addSubview_(collectionView)
    collectionView.translatesAutoresizingMaskIntoConstraints = False

    NSLayoutConstraint.activateConstraints_([
      collectionView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      collectionView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      collectionView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor, 0.8),
      collectionView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor, 0.8),
    ])

  @objc_method  # --- private
  def configureCellRegistration_(self, collectionView):

    @Block
    def configurationHandler(cell: objc_id, indexPath: objc_id,
                             item: objc_id) -> None:
      contentConfiguration = cell.defaultContentConfiguration

    cellRegistration = UICollectionViewCellRegistration.registrationWithCellClass_configurationHandler_(
      UICollectionViewListCell, configurationHandler)

    @Block
    def cellProvider(collectionView: objc_id, indexPath: objc_id,
                     identifier: objc_id) -> objc_id:
      return collectionView.dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_(
        cellRegistration, indexPath, identifier)

    return UICollectionViewDiffableDataSource.alloc(
    ).initWithCollectionView_cellProvider_(collectionView, cellProvider)

  @objc_method
  def initData(self):
    snapshot = NSDiffableDataSourceSnapshot.new()
    snapshot.appendSectionsWithIdentifiers_([0])
    snapshot.appendItemsWithIdentifiers_(['a',])
    self.modernDataSource.applySnapshot_animatingDifferences_(snapshot, True)

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print('viewWillAppear')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print('viewDidAppear')
    self.initData()

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print('viewWillDisappear')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print('viewDidDisappear')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'{__class__}: didReceiveMemoryWarning')


if __name__ == '__main__':
  from rbedge.functions import NSStringFromClass
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController

  main_vc = ModernCollectionViewViewController.new()
  _title = NSStringFromClass(ModernCollectionViewViewController)
  main_vc.navigationItem.title = _title

  presentation_style = UIModalPresentationStyle.fullScreen
  present_viewController(main_vc, presentation_style)

