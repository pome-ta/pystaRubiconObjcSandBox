from pyrubicon.objc.api import ObjCClass, objc_method
from pyrubicon.objc.types import CGRectMake

from rbedge.enumerations import UIProgressViewStyle
from rbedge import pdbr

from ._prototype import CustomTableViewCell

UIProgressView = ObjCClass('UIProgressView')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')


def add_prototype(identifier: str):

  def _create_reuse_dict(cellClass: CustomTableViewCell):
    prototypes.append({
      'cellClass': cellClass,
      'identifier': identifier,
    })

  return _create_reuse_dict


prototypes: list[dict[CustomTableViewCell, str]] = []


@add_prototype('defaultProgress')
class DefaultProgress(CustomTableViewCell):

  @objc_method
  def overrideCell(self):
    # todo: 一旦全部style は`default`
    progressView = UIProgressView.alloc().initWithProgressViewStyle_(
      UIProgressViewStyle.default)#.autorelease()

    progressView.translatesAutoresizingMaskIntoConstraints = False
    self.contentView.addSubview_(progressView)

    # xxx: `constraintGreaterThanOrEqualToAnchor` 後程確認
    NSLayoutConstraint.activateConstraints_([
      progressView.centerXAnchor.constraintEqualToAnchor_(
        self.contentView.centerXAnchor),
      progressView.centerYAnchor.constraintEqualToAnchor_(
        self.contentView.centerYAnchor),
      progressView.leadingAnchor.constraintEqualToAnchor_constant_(
        self.contentView.leadingAnchor, 20.0),
      progressView.trailingAnchor.constraintEqualToAnchor_constant_(
        self.contentView.trailingAnchor, -20.0),
    ])


@add_prototype('tintedProgress')
class TintedProgress(CustomTableViewCell):

  @objc_method
  def overrideCell(self):
    # todo: 一旦全部style は`default`
    progressView = UIProgressView.alloc().initWithProgressViewStyle_(
      UIProgressViewStyle.default)#.autorelease()

    progressView.translatesAutoresizingMaskIntoConstraints = False
    self.contentView.addSubview_(progressView)

    # xxx: `constraintGreaterThanOrEqualToAnchor` 後程確認
    NSLayoutConstraint.activateConstraints_([
      progressView.centerXAnchor.constraintEqualToAnchor_(
        self.contentView.centerXAnchor),
      progressView.centerYAnchor.constraintEqualToAnchor_(
        self.contentView.centerYAnchor),
      progressView.leadingAnchor.constraintEqualToAnchor_constant_(
        self.contentView.leadingAnchor, 20.0),
      progressView.trailingAnchor.constraintEqualToAnchor_constant_(
        self.contentView.trailingAnchor, -20.0),
    ])


@add_prototype('barProgress')
class BarProgress(CustomTableViewCell):

  @objc_method
  def overrideCell(self):
    # todo: 一旦全部style は`default`
    progressView = UIProgressView.alloc().initWithProgressViewStyle_(
      UIProgressViewStyle.default)#.autorelease()

    progressView.translatesAutoresizingMaskIntoConstraints = False
    self.contentView.addSubview_(progressView)

    # xxx: `constraintGreaterThanOrEqualToAnchor` 後程確認
    NSLayoutConstraint.activateConstraints_([
      progressView.centerXAnchor.constraintEqualToAnchor_(
        self.contentView.centerXAnchor),
      progressView.centerYAnchor.constraintEqualToAnchor_(
        self.contentView.centerYAnchor),
      progressView.leadingAnchor.constraintEqualToAnchor_constant_(
        self.contentView.leadingAnchor, 20.0),
      progressView.trailingAnchor.constraintEqualToAnchor_constant_(
        self.contentView.trailingAnchor, -20.0),
    ])