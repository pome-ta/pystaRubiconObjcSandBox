"""
note: まずは参照してるのやりきってみる
ref: [Diffable DataSource 入門 #Swift - Qiita](https://qiita.com/maiyama18/items/28039293b4bbf886ce8e)
  - Diffable DataSource

section で怒られてる
"""

import ctypes
from enum import IntEnum, auto

from pyrubicon.objc.api import ObjCClass, ObjCInstance, ObjCBlock, objc_method, objc_property, Block, at
from pyrubicon.objc.runtime import send_super, objc_id
from pyrubicon.objc.types import CGRectMake, NSInteger

from rbedge.enumerations import UICollectionLayoutListAppearance
from rbedge.functions import NSStringFromClass

# --- layout
UIViewController = ObjCClass('UIViewController')
UICollectionView = ObjCClass('UICollectionView')
UICollectionViewCompositionalLayout = ObjCClass(
  'UICollectionViewCompositionalLayout')
UICollectionLayoutListConfiguration = ObjCClass(
  'UICollectionLayoutListConfiguration')

# --- cell
UICollectionViewCellRegistration = ObjCClass(
  'UICollectionViewCellRegistration')
#UICollectionViewCell = ObjCClass('UICollectionViewCell')
UICollectionViewListCell = ObjCClass('UICollectionViewListCell')
UICellAccessoryCheckmark = ObjCClass('UICellAccessoryCheckmark')
NSIndexPath = ObjCClass('NSIndexPath')

# --- dataSource
UICollectionViewDiffableDataSource = ObjCClass(
  'UICollectionViewDiffableDataSource')

NSDiffableDataSourceSnapshot = ObjCClass('NSDiffableDataSourceSnapshot')

NSUUID = ObjCClass('NSUUID')
NSCollectionLayoutSection = ObjCClass('NSCollectionLayoutSection')

NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

CGRectZero = CGRectMake(0, 0, 0, 0)


class Todo:

  def __init__(self, id: NSUUID, title: str, done: bool):
    self.id = id
    self.title = title
    self.done = done

  @property
  def ID(self):
    return self.id


class Section(IntEnum):
  main = 0


class TodoRepository:

  def __init__(self):
    self.todos = [Todo(NSUUID.UUID(), f'Todo #{i}', False) for i in range(30)]
    self.todoIDs = [_todo.id for _todo in self.todos]

  def todo(self, id: Todo.ID) -> Todo:
    print(f'todo: {id=}')
    for _todo in self.todos:
      if id == _todo.id:
        return _todo


class TodoListViewController(UIViewController):
  #collectionView = objc_property(weak=True)
  #dataSource = objc_property()

  @objc_method
  def viewDidLoad(self):
    #
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    # --- Navigation
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title

    # xxx: 宣言する場所
    #self.repository = TodoRepository()

    self.configureCollectionView()
    self.configureDataSource()
    self.applySnapshot()

  @objc_method
  def viewDidAppear_(self, animated: bool):
    # xxx: 引数不要?
    send_super(__class__, self, 'viewDidAppear:')
    print('viewDidAppear')

  @objc_method
  def configureCollectionView(self):

    @Block
    def sectionProvider(sectionIndex: NSInteger,
                        _layoutEnvironment: objc_id) -> ctypes.c_void_p:
      print('Block: sectionProvider')
      # xxx: `sectionIndex`, 'NSInteger' ? `objc_id` ? `int` ?
      layoutEnvironment = ObjCInstance(_layoutEnvironment)

      #print(layoutEnvironment.container.effectiveContentSize.width)
      #pdbr.state(layoutEnvironment)
      #print(sectionIndex)
      _appearance = UICollectionLayoutListAppearance.plain
      configuration = UICollectionLayoutListConfiguration.alloc(
      ).initWithAppearance_(_appearance)

      layoutSection = NSCollectionLayoutSection.sectionWithListConfiguration_layoutEnvironment_(
        configuration, layoutEnvironment)

      #pdbr.state(layoutSection)
      return layoutSection

    layout = UICollectionViewCompositionalLayout.alloc(
    ).initWithSectionProvider_(sectionProvider)
    #pdbr.state(layout)
    #layout = UICollectionViewCompositionalLayout.alloc().initWithSection_(ObjCInstance(sectionProvider))

    self.collectionView = UICollectionView.alloc(
    ).initWithFrame_collectionViewLayout_(CGRectZero, layout)

    #pdbr.state(self.collectionView)

    self.view.addSubview_(self.collectionView)
    # --- Layout

    self.collectionView.translatesAutoresizingMaskIntoConstraints = False

    NSLayoutConstraint.activateConstraints_([
      self.collectionView.leadingAnchor.constraintEqualToAnchor_(
        self.view.leadingAnchor),
      self.collectionView.trailingAnchor.constraintEqualToAnchor_(
        self.view.trailingAnchor),
      self.collectionView.topAnchor.constraintEqualToAnchor_(
        self.view.topAnchor),
      self.collectionView.bottomAnchor.constraintEqualToAnchor_(
        self.view.bottomAnchor),
    ])

  @objc_method
  def configureDataSource(self):

    @Block
    def configurationHandler(_cell: objc_id, _indexPath: objc_id,
                             _item: objc_id) -> None:
      print('Block: configurationHandler')
      cell = ObjCInstance(_cell)
      indexPath = ObjCInstance(_indexPath)
      item = ObjCInstance(_item)

      configuration = cell.defaultContentConfiguration()
      configuration.setText_(item.title)
      cell.setContentConfiguration_(configuration)
      # xxx: UICellAccessoryCheckmark enum 確認
      cell.setAccessories_([
        UICellAccessoryCheckmark.alloc().init(),
      ])

    @Block
    def cellProvider(_collectionView: objc_id, _indexPath: objc_id,
                     _itemIdentifier: objc_id) -> ctypes.py_object:
      print('Block: cellProvider')
      collectionView = ObjCInstance(_collectionView)
      indexPath = ObjCInstance(_indexPath)
      itemIdentifier = ObjCClass(_itemIdentifier)
      #todo = self.repository.todo(itemIdentifier)
      dequeueConfiguredReusableCell = collectionView.dequeueConfiguredReusableCellWithRegistration_forIndexPath_item_(
        todoCellRegistration, indexPath, 'hoge')

      return dequeueConfiguredReusableCell

    todoCellRegistration = UICollectionViewCellRegistration.registrationWithCellClass_configurationHandler_(
      UICollectionViewListCell, configurationHandler)

    print('d')
    
    self.dataSource = UICollectionViewDiffableDataSource.alloc(
    ).initWithCollectionView_cellProvider_(self.collectionView, cellProvider)
    print(self.dataSource)

  @objc_method
  def applySnapshot(self):
    snapshot = NSDiffableDataSourceSnapshot.alloc().init()
    #snapshot.appendSectionsWithIdentifiers_([Section.main])
    #snapshot.appendSectionsWithIdentifiers_(at([int(Section.main)]))
    snapshot.appendSectionsWithIdentifiers_(at([0]))
    #snapshot.appendItemsWithIdentifiers_([NSUUID.UUID()])
    snapshot.appendItemsWithIdentifiers_intoSectionWithIdentifier_(
      at([]), Section.main)
    #snapshot.appendItemsWithIdentifiers_intoSectionWithIdentifier_(['a'], Section.main)
    #snapshot.appendItemsWithIdentifiers_(self.repository.todoIDs)
    #snapshot.appendItemsWithIdentifiers_([])
    #pdbr.state(snapshot)
    self.dataSource.applySnapshot_animatingDifferences_(snapshot, False)
    print('h')
    #pdbr.state(self.dataSource)
    #pdbr.state(self.collectionView)


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge import present_viewController
  from rbedge import pdbr

  todo_vc = TodoListViewController.new()
  style = UIModalPresentationStyle.fullScreen
  present_viewController(todo_vc, style)
  #print(CGRectZero)

