'''
  todo: 再度シンプルチャレンジ
'''
from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGRectMake

from rbedge.functions import NSStringFromClass
from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
UICollectionView = ObjCClass('UICollectionView')


class CollectionViewController(UIViewController):

  @objc_method
  def init(self):
    send_super(__class__, self, 'init')
    cg_zero = CGRectMake(0.0, 0.0, 0.0, 0.0)
    self.collectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(cg_zero, self.generateLayout())
  
  # --- private
  @objc_method
  def generateLayout(self) -> ObjCInstance:
    _appearance = UICollectionLayoutListAppearance.sidebar
    #_appearance = UICollectionLayoutListAppearance.plain
    listConfiguration = UICollectionLayoutListConfiguration.alloc(
    ).initWithAppearance_(_appearance)
    _headerMode = UICollectionLayoutListHeaderMode.firstItemInSection
    listConfiguration.headerMode = _headerMode
    layout = UICollectionViewCompositionalLayout.layoutWithListConfiguration_(
      listConfiguration)
    #pdbr.state(listConfiguration.appearance)
    #print(listConfiguration.appearance)
    return layout

if __name__ == '__main__':
  from rbedge import present_viewController
  from rbedge.enumerations import UIModalPresentationStyle

  vc = CollectionViewController.new()

  style = UIModalPresentationStyle.fullScreen
  #style = UIModalPresentationStyle.pageSheet
  present_viewController(vc, style)

