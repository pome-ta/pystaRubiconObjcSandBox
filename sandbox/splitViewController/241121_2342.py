'''
  note:
    [UICollectionViewでUITableViewのようなUIを実現する。ただし#available(iOS 14.0, *) #Swift - Qiita](https://qiita.com/sohichiro/items/9a3394551b8d76d2a346)
    事前確認
'''
import ctypes
from pyrubicon.objc.api import ObjCClass, ObjCProtocol, ObjCInstance, Block
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import send_super, objc_id

from rbedge.enumerations import (
  UIViewAutoresizing,
  UISplitViewControllerStyle,
  UISplitViewControllerColumn,
  UISplitViewControllerDisplayMode,
  UIModalPresentationStyle,
  UICollectionLayoutListAppearance,
)
from rbedge.objcMainThread import onMainThread
from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
UISplitViewController = ObjCClass('UISplitViewController')
UISplitViewControllerDelegate = ObjCProtocol('UISplitViewControllerDelegate')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

UIColor = ObjCClass('UIColor')
UILabel = ObjCClass('UILabel')
UIFont = ObjCClass('UIFont')

UINavigationController = ObjCClass('UINavigationController')  # todo: 型確認用

UICollectionView = ObjCClass('UICollectionView')
UICollectionViewLayout = ObjCClass('UICollectionViewLayout')
UICollectionLayoutListConfiguration = ObjCClass(
  'UICollectionLayoutListConfiguration')
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')
UICollectionViewCellRegistration = ObjCClass(
  'UICollectionViewCellRegistration')
UICollectionViewListCell = ObjCClass('UICollectionViewListCell')

UICollectionViewDiffableDataSource = ObjCClass(
  'UICollectionViewDiffableDataSource')
NSDiffableDataSourceSectionSnapshot = ObjCClass(
  'NSDiffableDataSourceSectionSnapshot')
NSDiffableDataSourceSnapshot = ObjCClass('NSDiffableDataSourceSnapshot')


class ViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    # --- Navigation
    title = NSStringFromClass(__class__)

    self.navigationItem.title = title

    # --- View
    collectionView = UICollectionView.alloc()

    self.configureLayout_(collectionView)

    self.view.addSubview_(collectionView)
    collectionView.autoresizingMask = UIViewAutoresizing.flexibleHeight | UIViewAutoresizing.flexibleWidth

    collectionView.backgroundColor = UIColor.systemDarkTealColor()

    #self.dataSource = self.configureCellRegistration_(collectionView)
    self.configureCellRegistration_(collectionView)
    

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    self.initData()

  @objc_method
  def configureLayout_(self, collectionView):
    configuration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(UICollectionLayoutListAppearance.plain)
    layout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      configuration)
    collectionView.initWithFrame_collectionViewLayout_(self.view.bounds,
                                                       layout)

  @objc_method
  def configureCellRegistration_(self, collectionView):

    @Block
    def cellRegistrationHandler(_cell: objc_id, _indexPath: objc_id,
                                _item: objc_id) -> None:
      '''
      cell = ObjCInstance(_cell)
      indexPath = ObjCInstance(_indexPath)
      item = ObjCInstance(_item)
      content = _cell.defaultContentConfiguration()
      content.text = _item
      cell.contentConfiguration = _content
      '''
      pass

    cellRegistration = UICollectionViewCellRegistration.registrationWithCellClass_configurationHandler_(
      UICollectionViewListCell, cellRegistrationHandler)

    '''
    @Block
    def cellProvider(_collectionView: objc_id, _indexPath: objc_id,
                     _item: int) -> ctypes.py_object:
      #collectionView = ObjCInstance(_collectionView)
      #indexPath = ObjCInstance(_indexPath)
      #item = ObjCInstance(_item)
      print('h')

      return collectionView.dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_(
        _cellRegistration, _indexPath, _item)
    '''
    
    #return UICollectionViewDiffableDataSource.alloc().initWithCollectionView_cellProvider_(collectionView, cellProvider)
    #self.dataSource = UICollectionViewDiffableDataSource.alloc().initWithCollectionView_cellProvider_(collectionView, cellProvider)
    self.dataSource = UICollectionViewDiffableDataSource.alloc().initWithCollectionView_cellProvider_(collectionView, Block(collectionView.dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_, ctypes.py_object, objc_id, objc_id,objc_id))

  @objc_method
  def initData(self):
    snapshot = NSDiffableDataSourceSnapshot.alloc().init()
    snapshot.appendSectionsWithIdentifiers_([0])
    '''
    snapshot.appendItemsWithIdentifiers_([
      '🍇',
      '🍈',
      '🍉',
      '🍊',
      '🍋',
    ])
    '''
    snapshot.appendItemsWithIdentifiers_(['hoge'])
    #snapshot.appendItemsWithIdentifiers_([])
    self.dataSource.applySnapshot_animatingDifferences_(snapshot, False)
    #pdbr.state(self.dataSource.collectionView())
    #print(self.dataSource.collectionView)
    #pdbr.state(self.dataSource.snapshot())


if __name__ == '__main__':
  from rbedge import present_viewController

  vc = ViewController.new()

  style = UIModalPresentationStyle.fullScreen
  #style = UIModalPresentationStyle.pageSheet
  present_viewController(vc, style)
  
