import functools

from pyrubicon.objc.api import Block, ObjCClass, ObjCInstance
from pyrubicon.objc.runtime import libobjc, objc_block, objc_id

from objc_frameworks.Dispatch import dispatch_get_main_queue

NSThread = ObjCClass('NSThread')


# --- Sync / Async ---
def _dispatch_call(func_name, queue, block_obj):
  _function = getattr(libobjc, func_name)
  if not _function.argtypes:
    _function.restype = None
    _function.argtypes = [
      objc_id,
      objc_block,
    ]
  _function(queue, block_obj)


def onMainThread(func=None, *, sync=True):
  if func is None:
    return functools.partial(onMainThread, sync=sync)

  @functools.wraps(func)
  def wrapper(*args, **kwargs):
    if NSThread.isMainThread:
      return func(*args, **kwargs)

    queue = dispatch_get_main_queue()
    results = []  # 戻り値キャプチャ用

    def task():
      res = func(*args, **kwargs)
      results.append(res)

    block = Block(task, None)

    if sync:
      _dispatch_call('dispatch_sync', queue, block)
      return results[0] if results else None
    else:
      _dispatch_call('dispatch_async', queue, block)
      return None  # asyncは戻り値なし

  return wrapper

