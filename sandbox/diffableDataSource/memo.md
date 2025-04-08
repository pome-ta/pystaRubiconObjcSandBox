# 📝 2025/04/07

## `NSObjectProtocol` ?

[NSDiffableDataSourceSnapshot | UIDiffableDataSource.rs - source](https://docs.rs/objc2-ui-kit/latest/src/objc2_ui_kit/generated/UIDiffableDataSource.rs.html#31)

`NSDiffableDataSourceSnapshot.alloc()initWithImpl_` 



# 📝 2025/04/07

[UICollectionViewCellRegistration | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uicollectionviewcellregistration)

[UICollectionViewListCell | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/uicollectionviewlistcell?language=objc)

[NSDiffableDataSourceSnapshot | Apple Developer Documentation](https://developer.apple.com/documentation/uikit/nsdiffabledatasourcesnapshotreference?language=objc)

引数を`id` で取るやつってあるか？

# 📝 2025/01/25

## Swift 実行のdump とか

`applySnapshot` したら、dataSource 側が変わるはず

```
snapshot---
--- dump
▿ UIKit.NSDiffableDataSourceSnapshot<Swift.Int, Swift.String>
  ▿ _implWrapper: UIKit.NSDiffableDataSourceSnapshot<Swift.Int, Swift.String>.(unknown context at $7ff806f2d4fc).ImplWrapper #0
    - impl: <__UIDiffableDataSourceSnapshot 0x60000021ada0: sectionCounts=<_UIDataSourceSnapshotter: 0x600000269e60; 1 section with item counts: [2] >; sections=[0x600000269be0]; identifiers=[0x600000269b60]> #1
      - super: NSObject
--- debugPrint
UIKit.NSDiffableDataSourceSnapshot<Swift.Int, Swift.String>(_implWrapper: UIKit.NSDiffableDataSourceSnapshot<Swift.Int, Swift.String>.(unknown context at $7ff806f2d4fc).ImplWrapper)
dataSource---
--- dump
▿ UIKit.NSDiffableDataSourceSnapshot<Swift.Int, Swift.String>
  ▿ _implWrapper: UIKit.NSDiffableDataSourceSnapshot<Swift.Int, Swift.String>.(unknown context at $7ff806f2d4fc).ImplWrapper #0
    - impl: <__UIDiffableDataSourceSnapshot 0x600000269c60: sectionCounts=<_UIDataSourceSnapshotter: 0x600000269c40; 0 sections with item counts: [] >; sections=[0x600000008c00]; identifiers=[0x600000008c00]> #1
      - super: NSObject
--- debugPrint
UIKit.NSDiffableDataSourceSnapshot<Swift.Int, Swift.String>(_implWrapper: UIKit.NSDiffableDataSourceSnapshot<Swift.Int, Swift.String>.(unknown context at $7ff806f2d4fc).ImplWrapper)
dataSource---
--- dump
▿ UIKit.NSDiffableDataSourceSnapshot<Swift.Int, Swift.String>
  ▿ _implWrapper: UIKit.NSDiffableDataSourceSnapshot<Swift.Int, Swift.String>.(unknown context at $7ff806f2d4fc).ImplWrapper #0
    - impl: <__UIDiffableDataSourceSnapshot 0x6000002759a0: sectionCounts=<_UIDataSourceSnapshotter: 0x600000275d80; 1 section with item counts: [2] >; sections=[0x600000269be0]; identifiers=[0x600000269b60]> #1
      - super: NSObject
--- debugPrint
UIKit.NSDiffableDataSourceSnapshot<Swift.Int, Swift.String>(_implWrapper: UIKit.NSDiffableDataSourceSnapshot<Swift.Int, Swift.String>.(unknown context at $7ff806f2d4fc).ImplWrapper)
```


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
