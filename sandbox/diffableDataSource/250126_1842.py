"""
  note: `UICollectionViewController` でやってみる
"""

import ctypes

from pyrubicon.objc.api import ObjCClass, Block
from pyrubicon.objc.api import objc_method, objc_property, NSString, NSNumber
from pyrubicon.objc.runtime import send_super, objc_id

from rbedge.enumerations import (
  UICollectionLayoutListAppearance, )

from rbedge import pdbr

UICollectionViewController = ObjCClass('UICollectionViewController')
UICollectionViewController.declare_property('dataSource')
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


class ModernCollectionViewViewController(UICollectionViewController):
  #datasource: UICollectionViewDiffableDataSource = objc_property(weak=True)

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print('\tdealloc')
    pass

  @objc_method
  def initWithCollectionViewLayout_(self, layout: objc_id):
    send_super(__class__,
               self,
               'initWithCollectionViewLayout:',
               layout,
               restype=objc_id,
               argtypes=[
                 objc_id,
               ])
    return self

  # MARK: - View Life Cycle
  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.configureCellRegistration()

  @objc_method  # --- private
  def configureCellRegistration(self):

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

    self.dataSource = UICollectionViewDiffableDataSource.alloc(
    ).initWithCollectionView_cellProvider_(
      self.collectionView,
      Block(
        lambda collectionView, indexPath, identifier: ObjCInstance(
          collectionView).
        dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_(
          cellRegistration, ObjCInstance(indexPath), identifier), objc_id, *[
            ctypes.c_void_p,
            ctypes.c_void_p,
            objc_id,
          ]))
    #self.dataSource.reorderingHandlers.canReorderItemHandler = Block(lambda item: True, ctypes.c_bool, objc_id)

    #pdbr.state(self.dataSource.reorderingHandlers.canReorderItemHandler)

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
    snapshot = NSDiffableDataSourceSnapshot.new()
    _section = NSNumber.numberWithInt_(0)
    snapshot.appendSectionsWithIdentifiers_([
      _section,
    ])

    snapshot.appendItemsWithIdentifiers_intoSectionWithIdentifier_([
      NSString.stringWithString_('a'),
      NSString.stringWithString_('b'),
    ], _section)

    #self.dataSource.applySnapshot_animatingDifferences_(snapshot, True)
    self.dataSource.setImpl_(snapshot.impl)
    #self.dataSource.applySnapshot_animatingDifferences_completion_(snapshot, True, None)
    #self.dataSource.applySnapshot_animatingDifferences_(snapshot, True)
    #pdbr.state(self.dataSource.snapshot())
    #pdbr.state(snapshot.impl)
    self.collectionView.reloadData()
    #pdbr.state(self.collectionView.reloadData)

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

  _appearance = UICollectionLayoutListAppearance.plain
  configuration = UICollectionLayoutListConfiguration.alloc(
  ).initWithAppearance_(_appearance)
  layout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
    configuration)

  main_vc = ModernCollectionViewViewController.alloc(
  ).initWithCollectionViewLayout_(layout)
  _title = NSStringFromClass(ModernCollectionViewViewController)
  main_vc.navigationItem.title = _title

  presentation_style = UIModalPresentationStyle.fullScreen
  present_viewController(main_vc, presentation_style)

