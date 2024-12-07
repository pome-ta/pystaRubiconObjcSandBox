import ui
#import pyrubicon.objc
from objc_util import ObjCClass, ObjCInstance, sel
from pyrubicon.objc.api import ObjCClass, ObjCInstance, Block
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super, objc_id,objc_block

# 必要なクラスをインポート
UICollectionView = ObjCClass('UICollectionView')
UICollectionViewFlowLayout = ObjCClass('UICollectionViewFlowLayout')
UICollectionViewCell = ObjCClass('UICollectionViewCell')
UICollectionViewDiffableDataSource = ObjCClass('UICollectionViewDiffableDataSource')
NSDiffableDataSourceSnapshot = ObjCClass('NSDiffableDataSourceSnapshot')
NSIndexPath = ObjCClass('NSIndexPath')

# セル用のカスタムクラス
class MyCollectionViewCell(ObjCClass('UICollectionViewCell')):
    def initWithFrame_(self, frame):
        self = ObjCInstance(self).initWithFrame_(frame)
        if not self:
            return None
        self.label = ObjCClass('UILabel').alloc().initWithFrame_(frame)
        self.label.setText_('Sample Item')
        self.addSubview_(self.label)
        return self

# UICollectionView のレイアウトを設定
layout = UICollectionViewFlowLayout.alloc().init()
layout.setItemSize_((100.0, 100.0))  # セルのサイズを設定
layout.setMinimumLineSpacing_(10.0)  # 行間隔
layout.setMinimumInteritemSpacing_(10.0)  # アイテム間隔

# UICollectionView のインスタンスを作成
frame = ((0, 0), (375, 667))  # 画面全体
collection_view = UICollectionView.alloc().initWithFrame_layout_(frame, layout)

# UICollectionViewDiffableDataSource を設定
class MyCollectionViewDataSource:
    def __init__(self):
        self.data_source = UICollectionViewDiffableDataSource.alloc().initWithCollectionViewCellProvider_(
            collection_view, self.cell_provider
        )

    def cell_provider(self, collection_view, index_path, item_identifier):
        cell = collection_view.dequeueReusableCellWithReuseIdentifier_forIndexPath_('Cell', index_path)
        if not cell:
            cell = MyCollectionViewCell.alloc().initWithFrame_(((0, 0), (100, 100)))  # セルを初期化
        cell.label.setText_(item_identifier)  # アイテムに基づいてテキストを設定
        return cell

    def apply_snapshot(self, items):
        snapshot = NSDiffableDataSourceSnapshot.alloc().init()
        snapshot.appendSections_(['Section 1'])  # セクションを追加
        snapshot.appendItems_(items, toSection='Section 1')  # アイテムをセクションに追加
        self.data_source.applySnapshot_(snapshot, animatingDifferences=True)

# データソースのインスタンスを作成
data_source = MyCollectionViewDataSource()

# UICollectionView の初期化とデータ適用
items = [f'Item {i+1}' for i in range(20)]  # アイテムリストを作成
data_source.apply_snapshot(items)  # データスナップショットを適用

# UICollectionView のデリゲートを設定
class MyCollectionViewDelegate:
    def collectionView_didSelectItemAtIndexPath_(self, collection_view, index_path):
        print(f'Item {index_path.row()} selected')

delegate = MyCollectionViewDelegate()
collection_view.setDelegate_(delegate)

# UICollectionView の表示
vc = ui.View(frame=(0, 0, 375, 667))
vc.add_subview(collection_view)
vc.present('sheet')

