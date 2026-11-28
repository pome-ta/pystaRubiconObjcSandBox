from pyrubicon.objc import (
  ObjCClass,
  ObjCInstance,
  objc_method,
)  # api
from pyrubicon.objc import send_super, objc_id  # runtime
from pyrubicon.objc import NSInteger  # types

from objc_frameworks.Foundation import NSStringFromClass

__all__: list[str] = [
  'PrototypeTableViewCell',
]

UITableViewCell = ObjCClass('UITableViewCell')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')


class PrototypeTableViewCell(UITableViewCell):

  @objc_method
  def dealloc(self) -> None:
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t\t\t- {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def initWithStyle_reuseIdentifier_(
    self,
    style: NSInteger,
    reuseIdentifier,
  ) -> ObjCInstance:
    #print(f'\t\t\t{NSStringFromClass(__class__)}: initWithStyle:reuseIdentifier:')
    super_args = [
      style,
      reuseIdentifier,
    ]
    super_argtypes = [
      NSInteger,
      objc_id,
    ]

    self = ObjCInstance(
      send_super(
        __class__,
        self,
        'initWithStyle:reuseIdentifier:',
        *super_args,
        restype=objc_id,
        argtypes=super_argtypes,
      ))
    if self is None:
      return None

    self.overrideCell()
    return self

  @objc_method
  def overrideCell(self) -> None:
    # todo: override用、継承先で記載
    # 継承先の`overrideCell` 内で、`self.addSubviewWithLayout_` を呼びlayout の仮確定
    # layout の詳細設定は、`overrideCell` 内の、`self.addSubviewWithLayout_` を呼んだ後に行う
    #print(f'\t\t\t{NSStringFromClass(__class__)}: prototype.overrideCell')
    pass

  # --- layout
  @objc_method
  def addSubviewWithLayout_(self, subView: ObjCInstance) -> None:
    # 要素（`subView`）をcontentView に追加設定と、layout の仮確定
    # layout の詳細設定は、`overrideCell` 内の、`self.addSubviewWithLayout_` を呼んだ後に行う
    self.contentView.addSubview_(subView)
    subView.translatesAutoresizingMaskIntoConstraints = False

    centerXAnchor = subView.centerXAnchor.constraintEqualToAnchor_(
      self.contentView.centerXAnchor)

    centerYAnchor = subView.centerYAnchor.constraintEqualToAnchor_(
      self.contentView.centerYAnchor)

    NSLayoutConstraint.activateConstraints_([
      centerXAnchor,
      centerYAnchor,
    ])

