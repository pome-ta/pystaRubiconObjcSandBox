from pyrubicon.objc.api import objc_const, ObjCInstance
from pyrubicon.objc.runtime import load_library

SceneKit = load_library('SceneKit')


def _get_const(global_variable_name) -> ObjCInstance:
  return objc_const(SceneKit, global_variable_name)

