if __name__ == '__main__':
  try:
    import bootstrap
  except ModuleNotFoundError as e:
    _TARGET_NAME = 'bootstrap'
    if e.name != _TARGET_NAME:
      raise
    import pathlib as _pathlib, runpy as _runpy

    _runpy.run_path(
      next(
        filter(
          _pathlib.Path.is_file,
          (_dir / f'{_TARGET_NAME}.py'
           for _dir in _pathlib.Path(__file__).resolve().parents),
        ),
        f'{_TARGET_NAME} not found',
      ))


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

prototypes: list[CellPrototype] = []
add_prototype = create_prototype_decorator(prototypes)


@add_prototype('buttonSystemAddContact')
class ButtonSystemAddContact(CustomTableViewCell):

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
    button.translatesAutoresizingMaskIntoConstraints = False

    self.contentView.addSubview_(button)

    NSLayoutConstraint.activateConstraints_([
      button.centerXAnchor.constraintEqualToAnchor_(
        self.contentView.centerXAnchor),
      button.centerYAnchor.constraintEqualToAnchor_(
        self.contentView.centerYAnchor),
    ])

