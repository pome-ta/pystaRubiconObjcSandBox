from ctypes import byref, cast, Structure, c_void_p
import functools

from rubicon.objc import ObjCClass
from rubicon.objc import ObjCInstance, Block
from rubicon.objc.runtime import objc_id, load_library

import pdbr

libSystem = load_library('System')
libdispatch = libSystem

dispatch_sync = libdispatch.dispatch_sync
dispatch_sync.restype = c_void_p
dispatch_sync.argtypes = [c_void_p, c_void_p]


class struct_dispatch_queue_s(Structure):
  pass  # No _fields_, because this is an opaque structure.


_dispatch_main_q = struct_dispatch_queue_s.in_dll(libdispatch,
                                                  '_dispatch_main_q')


def dispatch_get_main_queue():
  return ObjCInstance(cast(byref(_dispatch_main_q), objc_id))


UINavigationController = ObjCClass('UINavigationController')
UIViewController = ObjCClass('UIViewController')

UIColor = ObjCClass('UIColor')


def run_controller(view_controller):
  pass


#@Block

#dispatch_sync(dispatch_get_main_queue(), main)


def onmainthread(func):

  @functools.wraps(func)
  def new_func(*args, **kwargs):
    return func(*args, **kwargs)

  if ObjCClass('NSThread').isMainThread:
    return new_func
  else:
    return dispatch_sync(dispatch_get_main_queue(),
                         Block(new_func, None, c_void_p))


@onmainthread
def main(a) -> None:
  app = ObjCClass('UIApplication').sharedApplication
  window = app.keyWindow if app.keyWindow else app.windows[0]
  root_vc = window.rootViewController

  while root_vc.presentedViewController:
    root_vc = root_vc.presentedViewController

  vc = UIViewController.new()
  vc.view.setBackgroundColor_(UIColor.systemDarkRedColor())
  vc.setModalPresentationStyle_(1)
  root_vc.presentViewController_animated_completion_(vc, True, None)


main(a='h')

