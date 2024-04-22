"""
Abstract:
Test case element that serves our UITableViewCells.
UITableViewCells を提供するテスト ケース要素。
"""


class CaseElement:

  def __init__(self, title: str, cellID: str, configHandler):
    # セルの視覚的なタイトル (テーブル セクションのヘッダー タイトル)
    self.title = title
    # nib ファイル内でセルを検索するためのテーブルビューのセルの識別子。
    self.cellID = cellID
    # セルのサブビューを設定するための構成ハンドラー。
    # xxx: ガバガバ
    self.configHandler = configHandler

  @staticmethod
  def targetView(cell):
    # xxx: 多分まだ呼び出せない
    # xxx: index 呼び出しがスマートに書けるかも

    return cell.contentView().subviews().objectAtIndexedSubscript_(
      0) if cell != None else None

