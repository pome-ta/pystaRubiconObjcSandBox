from functools import partial


def add_prototype(identifier: str, prototypes: list):

  def _create_reuse_dict(cellClass):
    prototypes.append({
      'cellClass': cellClass,
      'identifier': identifier,
    })
    return cellClass

  return _create_reuse_dict


def create_prototype_decorator(prototypes: list):
  return partial(add_prototype, prototypes=prototypes)

