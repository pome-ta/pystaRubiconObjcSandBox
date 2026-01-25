from pyrubicon.objc.api import objc_const
from pyrubicon.objc.runtime import load_library

SceneKit = load_library('SceneKit')


def _get_const(global_variable_name) -> str:
  return str(objc_const(SceneKit, global_variable_name))


SCNPreferredRenderingAPIKey = _get_const('SCNPreferredRenderingAPIKey')

