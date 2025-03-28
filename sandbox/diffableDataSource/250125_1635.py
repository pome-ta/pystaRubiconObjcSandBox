"""
  note: [UICollectionViewでUITableViewのようなUIを実現する。ただし#available(iOS 14.0, *) #Swift - Qiita](https://qiita.com/sohichiro/items/9a3394551b8d76d2a346)
"""

import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import objc_method, NSString, NSNumber
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
UICollectionViewCell = ObjCClass('UICollectionViewCell')
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
    self.modernCollectionView = UICollectionView.alloc()
    self.configureLayout_(self.modernCollectionView)
    self.modernDataSource = self.configureCellRegistration_(
      self.modernCollectionView)

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
    def configurationHandler(_cell: ctypes.c_void_p,
                             _indexPath: ctypes.c_void_p,
                             _item: ctypes.c_void_p) -> None:
      cell = ObjCInstance(_cell)
      content = cell.defaultContentConfiguration()
      content.text = ObjCInstance(_item)
      cell.contentConfiguration = content

    cellRegistration = UICollectionViewCellRegistration.registrationWithCellClass_configurationHandler_(
      UICollectionViewListCell, configurationHandler)

    dataSource = UICollectionViewDiffableDataSource.alloc(
    ).initWithCollectionView_cellProvider_(
      collectionView,
      Block(
        lambda collectionView, indexPath, identifier: ObjCInstance(
          collectionView).
        dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_(
          cellRegistration, ObjCInstance(indexPath), identifier), objc_id, *[
            ctypes.c_void_p,
            ctypes.c_void_p,
            objc_id,
          ]))
    return dataSource

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
    #snapshot = NSDiffableDataSourceSnapshot.new()
    snapshot = self.modernDataSource.snapshot()

    _section = NSNumber.numberWithInt_(0)
    snapshot.appendSectionsWithIdentifiers_([
      _section,
    ])

    snapshot.appendItemsWithIdentifiers_intoSectionWithIdentifier_([
      NSString.stringWithString_('a'),
      NSString.stringWithString_('b'),
    ], _section)
    '''
    snapshot.appendItemsWithIdentifiers_([
      NSString.stringWithString_('a'),
      NSString.stringWithString_('b'),
    ])
    '''

    #pdbr.state(snapshot.impl)
    #pdbr.state(self.modernCollectionView)
    #pdbr.state(self.modernCollectionView)
    pdbr.state(self.modernDataSource.impl)
    '''
    self.modernCollectionView.reloadData()
    pdbr.state(self.modernCollectionView)
    print('---')
    print(self.modernDataSource)
    print('---')
    print(self.modernDataSource.snapshot())
    print('---')
    print(snapshot)
    '''
    '''
    print('snapshot')
    print(snapshot.impl)
    print('modernDataSource ---')
    print(self.modernDataSource.snapshot().impl)

    self.modernDataSource.applySnapshot_animatingDifferences_(snapshot, True)
    print('--- modernDataSource')
    print(self.modernDataSource.snapshot().impl)
    '''
    #self.modernDataSource.applySnapshot_toSection_animatingDifferences_(snapshot, _section, True)
    #pdbr.state(self.modernDataSource)
    #self.modernCollectionView.reloadData()
    #self.modernDataSource.applySnapshotUsingReloadData_(snapshot)

    #pdbr.state(self.modernDataSource.sectionIdentifierForIndex_(0))

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
    self.modernDataSource = None
    self.modernCollectionView = None
    #self.initData = None
    #self.cellRegistration = None
    #self.initData = None

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

