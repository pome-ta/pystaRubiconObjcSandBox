from pyrubicon.objc import ObjCClass, objc_method  # api
from pyrubicon.objc import send_super  # runtime

from objc_frameworks.Foundation import NSStringFromClass
from objc_frameworks.UIKit import UIButtonType, UIControlState

from rbedge import pdbr

from py_utils.add_prototype_decorator import (
  CellPrototype,
  create_prototype_decorator,
)
from py_utils.storyboard_prototype import PrototypeTableViewCell

__all__: list[str] = [
  'prototypes',
]

prototypes: list[CellPrototype] = []
add_prototype = create_prototype_decorator(prototypes)

UIButton = ObjCClass('UIButton')


@add_prototype('buttonSystemAddContact')
class ButtonSystemAddContact(PrototypeTableViewCell):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t\t- {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def overrideCell(self) -> None:
    send_super(
      __class__,
      self,
      'overrideCell',
      restype=None,
    )

    type = UIButtonType.contactAdd
    button = UIButton.buttonWithType_(type)

    # --- layout
    self.addSubviewWithLayout_(button)

