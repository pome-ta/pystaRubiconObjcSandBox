from functools import partial

# todo: 型チェック
from typing import TypedDict, TypeVar

from py_utils.storyboard_prototype import PrototypeTableViewCell

T = TypeVar('T', bound=PrototypeTableViewCell)


class CellPrototype(TypedDict):
  cellClass: type[PrototypeTableViewCell]
  identifier: str


def add_prototype(
  identifier: str,
  prototypes: list[CellPrototype],
):

  def _create_reuse_dict(cellClass):
    prototypes.append({
      'cellClass': cellClass,
      'identifier': identifier,
    })
    return cellClass

  return _create_reuse_dict


def create_prototype_decorator(prototypes: list[CellPrototype]):
  return partial(add_prototype, prototypes=prototypes)

