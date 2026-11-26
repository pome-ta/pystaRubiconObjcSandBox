from pyrubicon.objc import objc_const, ObjCInstance  # api
from pyrubicon.objc.runtime import load_library

framework = load_library('Metal')


def _get_const(global_variable_name) -> ObjCInstance:
  return objc_const(framework, global_variable_name)

