import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCProtocol, objc_method, objc_property
from pyrubicon.objc.runtime import send_super, load_library
from pyrubicon.objc.types import NSInteger, CGRect

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
UICollectionViewListCell = ObjCClass('UICollectionViewListCell')
UICollectionViewLayout = ObjCClass('UICollectionViewLayout')  # todo: 型呼び出し
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')
UICollectionLayoutListConfiguration = ObjCClass(
  'UICollectionLayoutListConfiguration')

UICollectionViewDataSource = ObjCProtocol('UICollectionViewDataSource')
UICollectionViewDelegate = ObjCProtocol('UICollectionViewDelegate')

CoreGraphics = load_library('CoreGraphics')
CGRectZero = CGRect.in_dll(CoreGraphics, 'CGRectZero')

# [UICollectionLayoutListConfigurationのheaderMode=.firstItemInSection観測隊](https://zenn.dev/samekard_dev/articles/2cbb0788915f01)
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
  collectionView = objc_property()
  cellId = objc_property()

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')

    self.cellId = 'Cell'
    '''

    listConfiguration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(UICollectionLayoutListAppearance.plain)
    listConfiguration.headerMode = UICollectionLayoutListHeaderMode.firstItemInSection

    simpleLayout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      listConfiguration)

    
    self.collectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(CGRectZero, simpleLayout)
    '''

    return self

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    self.view.backgroundColor = UIColor.systemDarkRedColor()

    listConfiguration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(UICollectionLayoutListAppearance.plain)
    listConfiguration.headerMode = UICollectionLayoutListHeaderMode.firstItemInSection

    simpleLayout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      listConfiguration)

    self.collectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(self.view.bounds, simpleLayout)

    self.collectionView.registerClass_forCellWithReuseIdentifier_(
      UICollectionViewListCell, self.cellId)

    self.collectionView.dataSource = self
    self.collectionView.delegate = self

    self.view.addSubview_(self.collectionView)
    autoresizingMask = UIViewAutoresizing.flexibleHeight | UIViewAutoresizing.flexibleWidth

    self.collectionView.autoresizingMask = autoresizingMask
    '''
    self.collectionView.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      self.collectionView.topAnchor.constraintEqualToAnchor_(
        self.view.safeAreaLayoutGuide.topAnchor),
      self.collectionView.bottomAnchor.constraintEqualToAnchor_(
        self.view.safeAreaLayoutGuide.bottomAnchor),
      self.collectionView.leadingAnchor.constraintEqualToAnchor_(
        self.view.safeAreaLayoutGuide.leadingAnchor),
      self.collectionView.trailingAnchor.constraintEqualToAnchor_(
        self.view.safeAreaLayoutGuide.trailingAnchor),
    ])
    '''

  @objc_method
  def configureCollectionView(self):
    pass

  @objc_method
  def configureDataSource(self):
    pass

  @objc_method
  def generateLayout(self):
    listConfiguration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(UICollectionLayoutListAppearance.sidebar)
    layout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      listConfiguration)
    return layout

  # --- UICollectionViewDataSource
  @objc_method
  def numberOfSectionsInCollectionView_(self, collectionView) -> NSInteger:
    return len(prefectures)

  @objc_method
  def collectionView_numberOfItemsInSection_(self, collectionView,
                                             section: NSInteger) -> NSInteger:

    return len(prefectures[section])

  @objc_method
  def collectionView_cellForItemAtIndexPath_(self, collectionView,
                                             indexPath) -> ctypes.c_void_p:
    cell = collectionView.dequeueReusableCellWithReuseIdentifier_forIndexPath_(
      self.cellId, indexPath)

    cellConfiguration = cell.defaultContentConfiguration()
    cellConfiguration.text = prefectures[indexPath.section][indexPath.row]
    cell.contentConfiguration = cellConfiguration
    return cell.ptr

  # --- UICollectionViewDelegate
  @objc_method
  def collectionView_didSelectItemAtIndexPath_(self, collectionView,
                                               indexPath):
    print(f'didSelect: {prefectures[indexPath.section][indexPath.row]}')


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  main_vc = OutlineViewController.new()

  present_viewController(main_vc)

