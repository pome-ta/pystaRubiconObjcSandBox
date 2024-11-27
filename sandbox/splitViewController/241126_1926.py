'''
  note:
    `UISplitViewController` と、`UITableView`
      - `UICollectionView` でやってみる？
'''
import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCProtocol, ObjCInstance
from pyrubicon.objc.api import objc_method, objc_property, objc_const
from pyrubicon.objc.runtime import send_super, objc_id, load_library
from pyrubicon.objc.types import CGRectMake

from rbedge.enumerations import (
  UISplitViewControllerStyle,
  UISplitViewControllerColumn,
  UISplitViewControllerDisplayMode,
  UIUserInterfaceSizeClass,
  UICollectionLayoutListAppearance,
  UICollectionLayoutListHeaderMode,
  UICellAccessoryOutlineDisclosureStyle,
)
from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIKit = load_library('UIKit')  # todo: `objc_const` 用
UIViewController = ObjCClass('UIViewController')
UINavigationController = ObjCClass('UINavigationController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- SplitView
UISplitViewController = ObjCClass('UISplitViewController')
UISplitViewControllerDelegate = ObjCProtocol('UISplitViewControllerDelegate')
UITableViewCell = ObjCClass('UITableViewCell')

# --- CollectionView
UICollectionView = ObjCClass('UICollectionView')
UICollectionViewDelegate = ObjCProtocol('UICollectionViewDelegate')
UICollectionViewDataSource = ObjCProtocol('UICollectionViewDataSource')
UICollectionLayoutListConfiguration = ObjCClass(
  'UICollectionLayoutListConfiguration')
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')
UICollectionViewListCell = ObjCClass('UICollectionViewListCell')
#UIListContentTextProperties = ObjCClass('UIListContentTextProperties')
UICellAccessory = ObjCClass('UICellAccessory')
UICellAccessoryOutlineDisclosure = ObjCClass(
  'UICellAccessoryOutlineDisclosure')
UIBackgroundConfiguration = ObjCClass('UIBackgroundConfiguration')
#pdbr.state(UICellAccessory.alloc())
#pdbr.state()
#print(UICellAccessoryOutlineDisclosure.alloc().style)
#a = UICellAccessoryOutlineDisclosure.alloc().init()

# --- others
UIColor = ObjCClass('UIColor')
UILabel = ObjCClass('UILabel')
UIFont = ObjCClass('UIFont')
UIImage = ObjCClass('UIImage')


class OutlineItem:

  def __init__(self,
               title: str,
               imageName: str,
               storyboardName: str = None,
               subitems: list = []):
    self.title = title
    self.subitems = subitems
    self.storyboardName = storyboardName
    self.imageName = imageName


prefectures = [
  ['北海道', '北海道'],
  ['東北', '青森', '岩手', '秋田', '宮城', '山形', '福島'],
  ['関東', '茨城', '栃木', '群馬', '埼玉', '千葉', '東京', '神奈川'],
  ['甲信越', '新潟', '長野', '山梨'],
  ['北陸', '富山', '石川', '福井'],
  ['東海', '岐阜', '静岡', '愛知', '三重'],
  ['近畿', '滋賀', '京都', '奈良', '大阪', '和歌山', '兵庫'],
  ['中国', '鳥取', '島根', '岡山', '広島', '山口'],
  ['四国', '香川', '徳島', '愛媛', '高知'],
  ['九州', '福岡', '佐賀', '長崎', '大分', '熊本', '宮崎', '鹿児島'],
  ['沖縄', '沖縄'],
]


class PrimaryCollectionViewController(UIViewController,
                                      protocols=[
                                        UICollectionViewDelegate,
                                        UICollectionViewDataSource,
                                      ]):

  collectionView: UICollectionView = objc_property()

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    self.collectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(CGRectMake(0.0, 0.0, 0.0, 0.0),
                                          self.generateLayout())

    self.collectionView.delegate = self
    self.collectionView.dataSource = self

    self.identifier_str = 'customCells'
    self.collectionView.registerClass_forCellWithReuseIdentifier_(
      UICollectionViewListCell, self.identifier_str)

    return self

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')

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

  @objc_method
  def numberOfSectionsInCollectionView_(self, collectionView) -> int:
    return len(prefectures)

  @objc_method
  def collectionView_numberOfItemsInSection_(self, collectionView,
                                             section: int) -> int:

    return len(prefectures[section])

  @objc_method
  def collectionView_cellForItemAtIndexPath_(self, collectionView,
                                             indexPath) -> objc_id:
    cell = collectionView.dequeueReusableCellWithReuseIdentifier_forIndexPath_(
      self.identifier_str, indexPath)

    cellConfiguration = cell.defaultContentConfiguration()
    cellConfiguration.text = prefectures[indexPath.section][indexPath.row]

    if indexPath.row:
      pass
    else:
      cellConfiguration.textProperties.font = UIFont.preferredFontForTextStyle_(
        str(objc_const(UIKit, 'UIFontTextStyleHeadline')))
      disclosureOptions = UICellAccessoryOutlineDisclosureStyle.header
      _outlineDisclosure = UICellAccessoryOutlineDisclosure.new()
      _outlineDisclosure.setStyle_(disclosureOptions)
      cell.accessories = [
        _outlineDisclosure,
      ]
      #[UICellAccessoryOutlineDisclosure.alloc().setStyle_()]
    #pdbr.state(cellConfiguration)
    background=UIBackgroundConfiguration.clearConfiguration()
    cell.backgroundConfiguration = background
    cell.contentConfiguration = cellConfiguration
    return cell

  # --- private
  @objc_method
  def generateLayout(self) -> ObjCInstance:
    _appearance = UICollectionLayoutListAppearance.sidebar
    #_appearance = UICollectionLayoutListAppearance.plain
    listConfiguration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(_appearance)
    _headerMode = UICollectionLayoutListHeaderMode.firstItemInSection
    #listConfiguration.headerMode = _headerMode
    #pdbr.state()
    layout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      listConfiguration)
    return layout


class SecondaryViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    # --- View
    self.view.backgroundColor = UIColor.systemDarkOrangeColor()

    self.label = UILabel.new()
    self.label.text = 'Primary'
    self.label.font = UIFont.systemFontOfSize_(26.0)
    self.label.sizeToFit()

    self.view.addSubview_(self.label)

    # --- Layout
    self.label.translatesAutoresizingMaskIntoConstraints = False

    NSLayoutConstraint.activateConstraints_([
      self.label.centerXAnchor.constraintEqualToAnchor_(
        self.view.centerXAnchor),
      self.label.centerYAnchor.constraintEqualToAnchor_(
        self.view.centerYAnchor),
    ])


class SplitViewController(UISplitViewController,
                          protocols=[
                            UISplitViewControllerDelegate,
                          ]):

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.delegate = self

    primary_vc = PrimaryCollectionViewController.new()
    #primary_vc = PrimaryTableViewController.new()
    primary_vc.title = primary_vc.className()

    secondary_vc = SecondaryViewController.new()

    primary = UISplitViewControllerColumn.primary
    secondary = UISplitViewControllerColumn.secondary

    self.setViewController_forColumn_(primary_vc, primary)
    self.setViewController_forColumn_(secondary_vc, secondary)

  # --- UISplitViewControllerDelegate
  @objc_method
  def splitViewController_topColumnForCollapsingToProposedTopColumn_(
      self, svc, proposedTopColumn: int) -> int:
    #return UISplitViewControllerColumn.secondary
    return UISplitViewControllerColumn.primary

  @objc_method
  def splitViewController_displayModeForExpandingToProposedDisplayMode_(
      self, svc, proposedDisplayMode: int):

    if (navController :=
        svc.viewControllers[0]).isMemberOfClass_(UINavigationController):
      navController.popToRootViewControllerAnimated_(False)
    return UISplitViewControllerDisplayMode.automatic


class ViewController(UIViewController):

  @objc_method
  def viewDidLoad(self):
    # --- Navigation
    send_super(__class__, self, 'viewDidLoad')
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    # --- View
    split = SplitViewController.alloc().initWithStyle_(
      UISplitViewControllerStyle.doubleColumn)
    self.addChildViewController_(split)
    self.view.addSubview_(split.view)
    split.didMoveToParentViewController_(self)

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #pdbr.state(self,1)
    #pdbr.state(self.childViewControllers[0])


if __name__ == '__main__':
  from rbedge import present_viewController
  from rbedge.enumerations import UIModalPresentationStyle

  vc = ViewController.new()

  style = UIModalPresentationStyle.fullScreen
  #style = UIModalPresentationStyle.pageSheet
  present_viewController(vc, style)

