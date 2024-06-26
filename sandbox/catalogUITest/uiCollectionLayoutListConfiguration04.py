import ctypes

from pyrubicon.objc.api import Block, ObjCClass, ObjCProtocol, objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import NSInteger

from rbedge.enumerations import (
  UICollectionLayoutListAppearance,
  UICollectionLayoutListHeaderMode,
  UIViewAutoresizing,
)
from rbedge.functions import NSStringFromClass

#ObjCClass.auto_rename = True

UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- UICollectionView
UICollectionView = ObjCClass('UICollectionView')
UICollectionViewCellRegistration = ObjCClass(
  'UICollectionViewCellRegistration')
UICollectionViewDiffableDataSource = ObjCClass('UICollectionViewDiffableDataSource')
UICollectionViewListCell = ObjCClass('UICollectionViewListCell')
#UICollectionViewLayout = ObjCClass('UICollectionViewLayout')  # todo: 型呼び出し
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')
UICollectionLayoutListConfiguration = ObjCClass(
  'UICollectionLayoutListConfiguration')

UICollectionViewDataSource = ObjCProtocol('UICollectionViewDataSource')
UICollectionViewDelegate = ObjCProtocol('UICollectionViewDelegate')


class OutlineItem:

  def __init__(self, title: str, subitems: list, storyboardName: str,
               imageName: str):
    self.title = title
    self.subitems = subitems
    self.storyboardName = storyboardName
    self.imageName = imageName


class OutlineViewController(UIViewController,
                            protocols=[
                              UICollectionViewDataSource,
                              UICollectionViewDelegate,
                            ]):
  outlineCollectionView = objc_property()

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    self.view.backgroundColor = UIColor.systemDarkRedColor()

    self.configureCollectionView()
    self.configureDataSource()

  # MARK: - UICollectionViewDiffableDataSource
  # --- extension OutlineViewController
  @objc_method
  def configureCollectionView(self):
    collectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(self.view.bounds,
                                          self.generateLayout())

    collectionView.backgroundColor = UIColor.systemDarkPurpleColor()

    self.view.addSubview_(collectionView)

    autoresizingMask = UIViewAutoresizing.flexibleHeight | UIViewAutoresizing.flexibleWidth
    collectionView.autoresizingMask = autoresizingMask
    self.outlineCollectionView = collectionView

  @objc_method
  def configureDataSource(self):

    @Block
    def configurationHandler(cell: objc_id, indexPath: objc_id,
                             menuItem: objc_id) -> None:
      print('h')

    containerCellRegistration = UICollectionViewCellRegistration.registrationWithCellClass_configurationHandler_(
      UICollectionViewListCell, configurationHandler)
    pdbr.state(UICollectionViewCellRegistration)
    #registrationWithCellClass_configurationHandler_
    #pdbr.state(UICollectionViewDiffableDataSource.alloc())
    #initWithCollectionView_sectionControllers_rendererIdentifierProvider_
    #pdbr.state(UICollectionView.alloc())

  @objc_method
  def generateLayout(self):
    listConfiguration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(UICollectionLayoutListAppearance.sidebar)
    layout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      listConfiguration)
    return layout


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  main_vc = OutlineViewController.new()

  present_viewController(main_vc)

