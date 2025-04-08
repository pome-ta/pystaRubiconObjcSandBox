""" note: 再度挑戦
[UICollectionViewでUITableViewのようなUIを実現する。ただし#available(iOS 14.0, *) #Swift - Qiita](https://qiita.com/sohichiro/items/9a3394551b8d76d2a346)
[モダンなUICollectionViewでシンプルなリストレイアウト その1 〜 概要](https://zenn.dev/samekard_dev/articles/43991e9321b6c9)
"""

import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import NSObjectProtocol, NSString
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGRectMake, NSInteger

from rbedge.enumerations import (
  UICollectionLayoutListAppearance, )

from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
UIColor = ObjCClass('UIColor')

UICollectionView = ObjCClass('UICollectionView')
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



class DataSourceSnapshot(metaclass=NSObjectProtocol):
  pass

class MainViewController(UIViewController):

  modernCollectionView: UICollectionView = objc_property()
  modernDataSource: UICollectionViewDiffableDataSource = objc_property()

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'- {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    #print(f'\t{NSStringFromClass(__class__)}: loadView')

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    #print(f'\t{NSStringFromClass(__class__)}: viewDidLoad')

    # --- Navigation
    self.navigationItem.title = NSStringFromClass(__class__) if (
      title := self.navigationItem.title) is None else title

    # --- UICollectionView setup
    self.configureHierarchy()
    self.modernDataSource = self.configureCellRegistration()

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewWillAppear_')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'\t{NSStringFromClass(__class__)}: viewDidAppear_')
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
    # print(f'\t{NSStringFromClass(__class__)}: viewWillDisappear_')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'\t{NSStringFromClass(__class__)}: viewDidDisappear_')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'{__class__}: didReceiveMemoryWarning')

  @objc_method
  def configureHierarchy(self):
    appearance = UICollectionLayoutListAppearance.plain
    configuration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(appearance)
    layout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      configuration)

    rectZero = CGRectMake(0.0, 0.0, 0.0, 0.0)
    modernCollectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(rectZero, layout)
    #modernCollectionView.backgroundColor = UIColor.systemDarkPurpleColor()

    # --- Layout
    self.view.addSubview_(modernCollectionView)
    modernCollectionView.translatesAutoresizingMaskIntoConstraints = False

    layoutMarginsGuide = self.view.layoutMarginsGuide
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    NSLayoutConstraint.activateConstraints_([
      modernCollectionView.centerXAnchor.constraintEqualToAnchor_(
        layoutMarginsGuide.centerXAnchor),
      modernCollectionView.centerYAnchor.constraintEqualToAnchor_(
        layoutMarginsGuide.centerYAnchor),
      modernCollectionView.widthAnchor.constraintEqualToAnchor_multiplier_(
        layoutMarginsGuide.widthAnchor, 0.1),
      modernCollectionView.heightAnchor.constraintEqualToAnchor_multiplier_(
        layoutMarginsGuide.heightAnchor, 0.1),
    ])
    self.modernCollectionView = modernCollectionView

  @objc_method  # --- private
  def configureCellRegistration(self):

    def configurationHandler(cell: objc_id, indexPath: objc_id,
                             item: objc_id) -> None:
      print(cell)

    cellRegistration = UICollectionViewCellRegistration.registrationWithCellClass_configurationHandler_(
      UICollectionViewListCell,
      Block(configurationHandler, None, *[
        objc_id,
        objc_id,
        objc_id,
      ]))

    dataSource = UICollectionViewDiffableDataSource.alloc(
    ).initWithCollectionView_cellProvider_(
      self.modernCollectionView,
      Block(
        lambda collectionView, indexPath, item: ObjCInstance(collectionView).
        dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_(
          cellRegistration, ObjCInstance(indexPath), item), objc_id, *[
            objc_id,
            objc_id,
            objc_id,
          ]))

    return dataSource  #ObjCInstance(dataSource)

  @objc_method
  def initData(self):
    snapshot = NSDiffableDataSourceSnapshot.new()
    snapshot.appendSectionsWithIdentifiers_([0])
    snapshot.appendItemsWithIdentifiers_(['a'])
    #self.modernDataSource.applySnapshot_animatingDifferences_(snapshot, True)
    #pdbr.state(self.modernDataSource)
    pdbr.state(snapshot)
    #pdbr.state(snapshot.state())
    #print(snapshot.state())
    #pdbr.state(self.modernCollectionView)
    #print(self.modernDataSource)

    #print(self.modernCollectionView)

    #pdbr.state(snapshot)
    #validateIdentifiers
    #sectionIdentifiers
    #snapshot.validateIdentifiers = (NSInteger, NSString)
    #print(snapshot.validateIdentifiers())
    #print('---')
    #print(snapshot.appendItemsWithIdentifiers_)
    #pdbr.state(NSObjectProtocol)
    #print(dir(NSObjectProtocol))


if __name__ == '__main__':
  from rbedge.app import App
  from rbedge.enumerations import UIModalPresentationStyle

  main_vc = MainViewController.new()

  #presentation_style = UIModalPresentationStyle.fullScreen
  presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()

