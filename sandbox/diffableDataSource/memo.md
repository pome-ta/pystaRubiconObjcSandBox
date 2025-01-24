# 📝 2025/01/24

## `NSIndexPath` のエラーで落ちる

- `appendItemsWithIdentifiers_` で、追加をすると落ちる
  - 追加しないと落ちない
  - `appendSectionsWithIdentifiers_` へは、複数入れても問題ない
- [Important | NSDiffableDataSourceSnapshot](https://developer.apple.com/documentation/uikit/nsdiffabledatasourcesnapshotreference?language=objc#:~:text=Important) の理解として、`NSNumber` や、`NSString` で呼び出しているつもりだけど、、、(`NSObject` をsubclassとしたHashable なもの)
- どこかの`Block` 処理の型がダメか？
  - `*` があるのは、ポインタ（？）として`objc_id` で良い？
    - `id` って、Rubicon だとどのように指定するのだろうか
      - `objc_id` で良さそう？
        - [objc_id | rubicon.objc.runtime — Low-level Objective-C runtime access - Rubicon 0.5.0](https://rubicon-objc.readthedocs.io/en/stable/reference/rubicon-objc-runtime.html#rubicon.objc.runtime.objc_id)
      - となると、他の引数の型を考えないといけないのか
  - `ObjCBlock` と、`objc_block` 使ってないな、、、


[NSDiffableDataSourceSnapshotReference | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/nsdiffabledatasourcesnapshotreference?language=objc)

[objc_id | rubicon.objc.runtime — Low-level Objective-C runtime access - Rubicon 0.5.0](https://rubicon-objc.readthedocs.io/en/stable/reference/rubicon-objc-runtime.html#rubicon.objc.runtime.objc_id)



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
