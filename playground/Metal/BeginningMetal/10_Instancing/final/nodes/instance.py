from pyrubicon.objc.api import objc_method, objc_property

from .node import Node
from .model import Model
from .renderable import Renderable

from simdTypes import ModelConstants


class Instance(Node):

  model: Model = objc_property()

  nodes: '[Node]()' = objc_property(object)
  instanceConstants: '[ModelConstants]()' = objc_property(object)

  modelConstants: ModelConstants = objc_property(object)

