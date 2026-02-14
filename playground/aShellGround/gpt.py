_TOP_DIR_NAME = 'pystaRubiconObjcSandBox'
_MODULES_DIR_NAME = 'modules'

# todo: `./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME}` にあるpackage のimport 準備
if __name__ == '__main__' and not __file__[:__file__.rfind('/')].endswith(
    _TOP_DIR_NAME):
  import pathlib
  import sys
  __parents = pathlib.Path(__file__).resolve().parents
  for __dir_path in __parents:
    if __dir_path.name == _TOP_DIR_NAME and (__modules_path := __dir_path /
                                             _MODULES_DIR_NAME).exists():
      sys.path.insert(0, str(__modules_path))
      break
  else:
    import warnings
    with warnings.catch_warnings():
      warnings.simplefilter('always', ImportWarning)
      __warning_message = f'./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME} not found in parent directories'
      warnings.warn(__warning_message, ImportWarning)

import ctypes
import ctypes

from pyrubicon.objc import ObjCClass, objc_method
from pyrubicon.objc.runtime import (
    SEL,
    send_message,
    objc_id,
)


# --- UIKit classes ---
UIApplication = ObjCClass("UIApplication")
UIViewController = ObjCClass("UIViewController")
UIColor = ObjCClass("UIColor")
dispatch_async = ctypes.CDLL(None).dispatch_async
dispatch_get_main_queue = ctypes.CDLL(None).dispatch_get_main_queue


# --- 自前 ViewController ---
class MyViewController(UIViewController):

    @objc_method
    def viewDidLoad(self) -> None:
        self.view.backgroundColor = UIColor.redColor()


# --- topMost VC 取得 ---
def top_view_controller(root):
    vc = root
    while vc.presentedViewController:
        vc = vc.presentedViewController
    return vc


# --- main thread で present ---
def present_on_main():
    app = UIApplication.sharedApplication

    # iOS13+ 対応 window 取得
    scenes = app.connectedScenes.allObjects
    scene = scenes[0]
    window = scene.windows[0]

    root = window.rootViewController
    vc = MyViewController.alloc().init()

    top = top_view_controller(root)

    send_message(
        top,
        SEL("presentViewController:animated:completion:"),
        vc,
        True,
        None,
        restype=None,
        argtypes=[objc_id, ctypes.c_bool, objc_id],
    )


# --- GCD で main thread 実行 ---
BLOCK = ctypes.CFUNCTYPE(None)

def run():
    present_on_main()

dispatch_async(dispatch_get_main_queue(), BLOCK(run))
