'''
  note: 
    - [【Swift】世界一わかりやすいTableViewのアコーディオンの実装方法 #Xode - Qiita](https://qiita.com/tosh_3/items/c254429f4f68c7eab39d)
    - `UICollectionView` 形式にもっていく
      - 
'''

import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCProtocol, ObjCInstance
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id, SEL
from pyrubicon.objc.types import NSInteger

from rbedge.enumerations import (
  UICollectionLayoutListAppearance,
  UICollectionLayoutListHeaderMode,
  UITableViewStyle,
  UITableViewRowAnimation,
)
from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- TableView
UITableView = ObjCClass('UITableView')
UITableViewCell = ObjCClass('UITableViewCell')
UITableViewHeaderFooterView = ObjCClass('UITableViewHeaderFooterView')
UITableViewDataSource = ObjCProtocol('UITableViewDataSource')
UITableViewDelegate = ObjCProtocol('UITableViewDelegate')

UITapGestureRecognizer = ObjCClass('UITapGestureRecognizer')
NSIndexSet = ObjCClass('NSIndexSet')

# --- UICollectionView
UICollectionView = ObjCClass('UICollectionView')
UICollectionLayoutListConfiguration = ObjCClass(
  'UICollectionLayoutListConfiguration')
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')
UICollectionViewListCell = ObjCClass('UICollectionViewListCell')
UICollectionReusableView = ObjCClass('UICollectionReusableView')

# --- others
UIColor = ObjCClass('UIColor')


class Rail:

  def __init__(self, railName: str, stationArray: list, isShown: bool = True):
    self.isShown = isShown
    self.railName = railName
    self.stationArray = stationArray



headerArray = ['山手線', '東横線', '田園都市線', '常磐線',] # yapf: disable
yamanoteArray = ['渋谷', '新宿', '池袋',] # yapf: disable
toyokoArray = ['自由ヶ丘', '日吉',] # yapf: disable
dentoArray = ['溝の口', '二子玉川',] # yapf: disable
jobanArray = ['上野',] # yapf: disable


courseArray = [
  Rail(rail, stations) for rail, stations in zip(headerArray, [
    yamanoteArray,
    toyokoArray,
    dentoArray,
    jobanArray,
  ])
]

items = [
  'hoge',
]


class ViewController(UIViewController):

  tableView: UITableView = objc_property()
  collectionView: UICollectionView = objc_property()

  @objc_method
  def viewDidLoad(self):
    # --- Navigation
    send_super(__class__, self, 'viewDidLoad')
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    # --- View
    self.view.backgroundColor = UIColor.systemBrownColor()  # todo: 確認用

    # --- collection set
    self.listCell_identifier = 'customListCell'
    self.header_section = 'headerSection'
    self.supplementaryView_identifier = 'customSupplementary'
    collectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(self.view.bounds,
                                          self.generateLayout())
    collectionView.registerClass_forCellWithReuseIdentifier_(
      UICollectionViewListCell, self.listCell_identifier)

    collectionView.registerClass_forSupplementaryViewOfKind_withReuseIdentifier_(
      UICollectionReusableView, self.header_section, self.supplementaryView_identifier)

    pdbr.state(collectionView)
    #collectionView.delegate = self
    collectionView.dataSource = self

    # --- Layout
    self.view.addSubview_(collectionView)
    collectionView.translatesAutoresizingMaskIntoConstraints = False
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide
    NSLayoutConstraint.activateConstraints_([
      collectionView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      collectionView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      collectionView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor, 1.0),
      collectionView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor, 1.0),
    ])
    self.collectionView = collectionView

  # --- UICollectionViewDataSource
  @objc_method
  def numberOfSectionsInCollectionView_(self, collectionView) -> int:
    return len(courseArray)

  @objc_method
  def collectionView_numberOfItemsInSection_(self, collectionView,
                                             section: int) -> int:

    #return len(courseArray)
    return len(rail.stationArray) if (rail :=
                                      courseArray[section]).isShown else 0

  @objc_method
  def collectionView_cellForItemAtIndexPath_(self, collectionView,
                                             indexPath) -> objc_id:
    cell = collectionView.dequeueReusableCellWithReuseIdentifier_forIndexPath_(
      self.listCell_identifier, indexPath)

    cellConfiguration = cell.defaultContentConfiguration()
    cellConfiguration.text = courseArray[indexPath.section].stationArray[
      indexPath.row]
    cell.contentConfiguration = cellConfiguration
    return cell

  @objc_method
  def collectionView_viewForSupplementaryElementOfKind_atIndexPath_(
      collectionView, kind, indexPath):
    #cell = collectionView.dequeueConfiguredReusableSupplementaryViewWithRegistration_forIndexPath_(self.supplementaryView_identifier, indexPath)
    cell = collectionView.dequeueReusableSupplementaryViewOfKind_withReuseIdentifier_forIndexPath_(self.header_section,self.supplementaryView, indexPath)
    #dequeueReusableSupplementaryViewOfKind_withReuseIdentifier_forIndexPath_
    return cell


  # --- private
  @objc_method
  def generateLayout(self) -> ObjCInstance:
    #_appearance = UICollectionLayoutListAppearance.plain
    _appearance = UICollectionLayoutListAppearance.sidebar
    listConfiguration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(_appearance)
    #_headerMode = UICollectionLayoutListHeaderMode.firstItemInSection
    _headerMode = UICollectionLayoutListHeaderMode.supplementary
    listConfiguration.headerMode = _headerMode

    layout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      listConfiguration)
    return layout


if __name__ == '__main__':
  from rbedge import present_viewController
  from rbedge.enumerations import UIModalPresentationStyle

  vc = ViewController.new()

  style = UIModalPresentationStyle.fullScreen
  #style = UIModalPresentationStyle.pageSheet
  present_viewController(vc, style)

