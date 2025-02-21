from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import objc_id, send_super

from rbedge.functions import NSStringFromClass
from rbedge import pdbr

from ._prototype import CustomTableViewCell

UIView = ObjCClass('UIView')
UIColor = ObjCClass('UIColor')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')


def add_prototype(identifier: str):

  def _create_reuse_dict(cellClass: CustomTableViewCell):
    prototypes.append({
      'cellClass': cellClass,
      'identifier': identifier,
    })

  return _create_reuse_dict


prototypes: list[dict[CustomTableViewCell | str, str]] = []


@add_prototype('hoge')
class Hoge(CustomTableViewCell):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t\t- {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def overrideCell(self) -> None:
    send_super(__class__, self, 'overrideCell')

    newView = UIView.new()
    newView.backgroundColor = UIColor.systemDarkPurpleColor()

    newView.translatesAutoresizingMaskIntoConstraints = False
    self.contentView.addSubview_(newView)

    NSLayoutConstraint.activateConstraints_([
      newView.heightAnchor.constraintEqualToConstant_(42.0),
      newView.widthAnchor.constraintEqualToConstant_(42.0),
      newView.centerXAnchor.constraintEqualToAnchor_(
        self.contentView.centerXAnchor),
      newView.centerYAnchor.constraintEqualToAnchor_(
        self.contentView.centerYAnchor),
    ])


@add_prototype('fuga')
class Fuga(CustomTableViewCell):

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'\t\t- {NSStringFromClass(__class__)}: dealloc')

  @objc_method
  def overrideCell(self) -> None:
    send_super(__class__, self, 'overrideCell')

    newView = UIView.new()
    newView.backgroundColor = UIColor.systemDarkTealColor()

    newView.translatesAutoresizingMaskIntoConstraints = False
    self.contentView.addSubview_(newView)

    NSLayoutConstraint.activateConstraints_([
      newView.heightAnchor.constraintEqualToConstant_(42.0),
      newView.widthAnchor.constraintEqualToConstant_(42.0),
      newView.centerXAnchor.constraintEqualToAnchor_(
        self.contentView.centerXAnchor),
      newView.centerYAnchor.constraintEqualToAnchor_(
        self.contentView.centerYAnchor),
    ])

