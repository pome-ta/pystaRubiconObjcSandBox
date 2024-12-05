# 📝 2024/12/05

- [UITableViewDiffableDataSource: example in Objective-C | Apple Developer Forums](https://forums.developer.apple.com/forums/thread/652551)



# 📝 2024/12/03

- [【Swift】UICollectionViewの更新処理には段階がある #iOS - Qiita](https://qiita.com/juginon/items/5526e7b79edadd2362b5)


# 📝 2024/11/30


- [The Developer's Guide to Cell Content Configuration in iOS 14 - BiTE Interactive](https://www.biteinteractive.com/cell-content-configuration-in-ios-14/)
- [Collection View Content Configuration in iOS 14 - BiTE Interactive](https://www.biteinteractive.com/collection-view-content-configuration-in-ios-14/)
- [Collection View Lists in iOS 14 - BiTE Interactive](https://www.biteinteractive.com/collection-view-lists-in-ios-14/)
- [Collection View Outlines in iOS 14 - BiTE Interactive](https://www.biteinteractive.com/collection-view-outlines-in-ios-14/)
- 


# 📝 2024/10/24

## `NSDiffableDataSourceSnapshot` 周辺

- `objc_property` っていらない？
  - 外部として参照しないんよな

# 📝 2024/05/14

`0.4.9`

## storyboard

`ButtonViewController.storyboard`


`reuseIdentifier` をどう捌くか？


サイズはよしなにやってもらう？



# 📝 2024/05/09


[なぜUITableViewControllerを使うなと言われるのか #iOS - Qiita](https://qiita.com/yosshi4486/items/33132718a0fb08273a45)






# 📝 2024/04/24

改めてstoryboard について考えてみる

- storyboard 内で完成をさせて、出せるようにする
  - 今回の場合は、`tests` の中で出せるようにしたい
  - 私の場合だと、`prototypes` の中を実装する
  - 




# 📝 2024/04/23

作業ログをしっかりとる

# 📝 2024/04/21

## `caseElement.py`

コピペした、呼び出し方法を書き換えないと

## 次は？storyboard かな？

作成手順を忘れた




# 📝 2024/04/19

## 運用想定

ディレクトリ直下には、Catalog としてのファイルを入れていく。Rubicon のためとしてのファイルは、`rbedge` にゴリゴリと入れていく

直下はあくまでも、Catalog のサンプル内容とイコールな関係としていきたい

## `rbedge`

独自のRubicon のライブラリとして、作ったファイルを置いていく

### 命名理由

Rubicon が多分「川」の意味があると思われるので、川の「端」として、「edge」 で、Rubicon の「r」と「b」 を付けて「rbedge」 とした。
ざっとググって、名前が被らないかは確認した。

### 運用方法

Python として正しくはないかもだけど、`pyrubicon` モジュールを読み込みをするので、直下に`test` ディレクトリを作成して、そのディレクトリ内で挙動の確認をする。

読み込みは、`sys` モジュールで無理やりpath を取得する流れ。

## ファイルの配置やら関連性について

rootNav 系を先に準備したが、実行するためとすると、裏側での動きだから、他のもの準備した方がいいのではないかと思う。

あと、定数ではなくenum をひとつひとつ書いていくしかないのかなぁというお気持ち
