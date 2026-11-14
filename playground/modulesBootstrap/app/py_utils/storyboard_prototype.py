from pyrubicon.objc import (
  ObjCClass,
  ObjCInstance,
  objc_method,
)  # api
from pyrubicon.objc import send_super, objc_id  # runtime
from pyrubicon.objc import NSInteger  # types

from objc_frameworks.Foundation import NSStringFromClass

from rbedge import pdbr

UITableViewCell = ObjCClass('UITableViewCell')


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

    send_super(
      __class__,
      self,
      'initWithStyle:reuseIdentifier:',
      *super_args,
      restype=objc_id,
      argtypes=super_argtypes,
    )

    self.overrideCell()
    return self

  @objc_method
  def overrideCell(self) -> None:
    # todo: override用、継承先で記載
    #print(f'\t\t\t{NSStringFromClass(__class__)}: prototype.overrideCell')
    pass

