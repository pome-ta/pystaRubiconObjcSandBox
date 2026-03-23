import ctypes

from pyrubicon.objc.api import ObjCInstance
from pyrubicon.objc.runtime import objc_id

from .constants import framework as MetalKit


def MTKModelIOVertexDescriptorFromMetal(
    metalDescriptor: objc_id) -> ObjCInstance:
  _function = MetalKit.MTKModelIOVertexDescriptorFromMetal
  _function.restype = objc_id
  _function.argtypes = [
    objc_id,
  ]

  return ObjCInstance(_function(metalDescriptor))

