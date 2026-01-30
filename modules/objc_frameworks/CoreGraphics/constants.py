from pyrubicon.objc.api import objc_const, ObjCInstance
from pyrubicon.objc.runtime import load_library

CoreGraphics = load_library('CoreGraphics')


def _get_const(global_variable_name) -> ObjCInstance:
  return objc_const(CoreGraphics, global_variable_name)

