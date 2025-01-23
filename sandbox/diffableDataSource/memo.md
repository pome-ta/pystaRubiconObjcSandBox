# 📝 2025/01/23

## DataSource

- `UICollectionViewDataSource`
- `UITableViewDiffableDataSource`


## UICollectionViewDiffableDataSource のobjc がいつも見つからないので
[UICollectionViewDiffableDataSource | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uicollectionviewdiffabledatasourcereference?language=objc)


## `UICollectionView`, `UICollectionViewDiffableDataSource`, `NSDiffableDataSourceSnapshot` のわからんところ

- `<``>` 山括弧で宣言って、rubicon だとどうゆこと？
- `cellProvider` 周りのBlock の型ってどれが正解？
- エラーログは、どの場面で発生しているのだ？
  - `[NSIndexPath _hasBeenReused]: unrecognized selector sent to instance 0x...`
- `pystaUIKitCatalogChallenge` の`outlineViewController.py` は、`dataSource` を使い達成できている。
  - [pystaUIKitCatalogChallenge/outlineViewController.py at main · pome-ta/pystaUIKitCatalogChallenge · GitHub](https://github.com/pome-ta/pystaUIKitCatalogChallenge/blob/main/outlineViewController.py)
  - この実装だと、矢印タップのアニメーションが実装できない（？）



# 📝 2024/12/06

- [モダンなUICollectionViewでシンプルなリストレイアウト その1 〜 概要](https://zenn.dev/samekard_dev/articles/43991e9321b6c9)
- [Building an Expandable List Using UICollectionView: Part 1](https://swiftsenpai.com/development/collectionview-expandable-list-part1/)
