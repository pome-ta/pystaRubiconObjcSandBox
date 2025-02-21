from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method
from pyrubicon.objc.runtime import objc_id, send_super

from rbedge.functions import NSStringFromClass
from rbedge import pdbr

from ._prototype import CustomTableViewCell

UIView = ObjCClass('UIView')
UILabel = ObjCClass('UILabel')
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
    #newView.backgroundColor = UIColor.systemDarkPurpleColor()
    
    
    newLabel = UILabel.new()
    newLabel.text = '変化前'
    newLabel.translatesAutoresizingMaskIntoConstraints = False
    self.contentView.addSubview_(newLabel)
    NSLayoutConstraint.activateConstraints_([
      newLabel.heightAnchor.constraintEqualToConstant_(32.0),
      newLabel.widthAnchor.constraintEqualToConstant_(64.0),
      newLabel.centerXAnchor.constraintEqualToAnchor_(
        self.contentView.centerXAnchor),
      newLabel.centerYAnchor.constraintEqualToAnchor_(
        self.contentView.centerYAnchor),
    ])
    
    
    
    '''

    newLabel.translatesAutoresizingMaskIntoConstraints = False
    newView.addSubview_(newLabel)

    NSLayoutConstraint.activateConstraints_([
      newLabel.widthAnchor.constraintEqualToAnchor_multiplier_(
        newView.widthAnchor, 1.0),
      newLabel.heightAnchor.constraintEqualToAnchor_multiplier_(
        newView.heightAnchor, 1.0),
    ])

    newView.translatesAutoresizingMaskIntoConstraints = False
    self.contentView.addSubview_(newView)

    NSLayoutConstraint.activateConstraints_([
      newView.heightAnchor.constraintEqualToConstant_(32.0),
      newView.widthAnchor.constraintEqualToConstant_(64.0),
      newView.centerXAnchor.constraintEqualToAnchor_(
        self.contentView.centerXAnchor),
      newView.centerYAnchor.constraintEqualToAnchor_(
        self.contentView.centerYAnchor),
    ])
    '''


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

