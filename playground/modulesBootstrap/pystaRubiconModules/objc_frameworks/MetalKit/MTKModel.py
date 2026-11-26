from pyrubicon.objc import ObjCInstance  # api
from pyrubicon.objc import objc_id  # runtime

from .constants import framework as MetalKit


def MTKModelIOVertexDescriptorFromMetal(
    metalDescriptor: objc_id) -> ObjCInstance:
  try:
    _func = MTKModelIOVertexDescriptorFromMetal._cfunc
  except AttributeError:
    _func = MetalKit.MTKModelIOVertexDescriptorFromMetal
    _func.restype = objc_id
    _func.argtypes = [
      objc_id,
    ]
    MTKModelIOVertexDescriptorFromMetal._cfunc = _func

  return ObjCInstance(_func(metalDescriptor))


def MTKMetalVertexDescriptorFromModelIO(
    modelIODescriptor: objc_id) -> ObjCInstance:
  try:
    _func = MTKMetalVertexDescriptorFromModelIO._cfunc
  except AttributeError:
    _func = MetalKit.MTKMetalVertexDescriptorFromModelIO
    _func.restype = objc_id
    _func.argtypes = [
      objc_id,
    ]
    MTKMetalVertexDescriptorFromModelIO._cfunc = _func

  return ObjCInstance(_func(modelIODescriptor))

