import ctypes

from pyrubicon.objc.api import ObjCClass, ObjCProtocol, objc_method, objc_property, objc_const
from pyrubicon.objc.runtime import send_super, objc_id, load_library
from pyrubicon.objc.types import NSInteger, NSZeroPoint

from rbedge.enumerations import UICollectionLayoutListAppearance, UICollectionLayoutListHeaderMode
from rbedge.functions import NSStringFromClass

#ObjCClass.auto_rename = True

UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- UICollectionView
UICollectionView = ObjCClass('UICollectionView')
UICollectionViewListCell = ObjCClass('UICollectionViewListCell')
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')
UICollectionLayoutListConfiguration = ObjCClass(
  'UICollectionLayoutListConfiguration')

UICollectionViewDataSource = ObjCProtocol('UICollectionViewDataSource')
#UICollectionViewLayout = ObjCClass('UICollectionViewLayout')

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


class ViewController(UIViewController,
                     protocols=[
                       UICollectionViewDataSource,
                     ]):
  collectionView = objc_property()

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    listConfiguration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(UICollectionLayoutListAppearance.plain)
    listConfiguration.headerMode = UICollectionLayoutListHeaderMode.firstItemInSection

    simpleLayout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      listConfiguration)

    #pdbr.state(UICollectionView.alloc())
    #self.collectionView =
    #z = objc_const(load_library('CoreGraphics'), 'CGRectZero')
    core = load_library('CoreGraphics')
    z = objc_const(core, )
    print(core)
    #UICollectionView.alloc().initWithFrame_collectionViewLayout_(NSZeroPoint, simpleLayout)
    return self


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  main_vc = ViewController.new()

  present_viewController(main_vc)

