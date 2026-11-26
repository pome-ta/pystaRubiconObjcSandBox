import functools

from pyrubicon.objc import (
  Block,
  ObjCClass,
  ObjCInstance,
)  # api
from pyrubicon.objc import objc_block, objc_id  # runtime
from pyrubicon.objc.runtime import libobjc

from objc_frameworks.Dispatch import (
  dispatch_get_main_queue,
  dispatch_sync,
  dispatch_async,
)

NSThread = ObjCClass('NSThread')


def onMainThread(func):

  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    if NSThread.isMainThread:
      func(*args, **kwargs)
      return
    block = Block(functools.partial(func, *args, **kwargs), None)
    dispatch_async(dispatch_get_main_queue(), block)

  return wrapper


'''
# wip: 要検討
def onMainThread(func=None, *, sync=True):
  if func is None:
    return functools.partial(onMainThread, sync=sync)

  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    if NSThread.isMainThread:
      func(*args, **kwargs)
      return 

    queue = dispatch_get_main_queue()
    results = []  # 戻り値キャプチャ用

    def task():
      res = func(*args, **kwargs)
      results.append(res)

    block = Block(task, None)

    if sync:
      dispatch_sync(queue, block)
      return results[0] if results else None
    else:
      dispatch_async(queue, block)
      return None  # asyncは戻り値なし

  return wrapper
'''

