from pyrubicon.objc.api import objc_const, ObjCInstance
from pyrubicon.objc.runtime import load_library

Metal = load_library('Metal')


def _get_const(global_variable_name) -> ObjCInstance:
  return objc_const(Metal, global_variable_name)

