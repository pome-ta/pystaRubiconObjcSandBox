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

#import asyncio
#from pyrubicon.objc.eventloop import RubiconEventLoop, EventLoopPolicy

__all__ = [
  'loop',
]

from pyrubicon.objc.api import ObjCClass
UIApplication = ObjCClass('UIApplication')

print('# ---')
'''
try:
  print('try s: loop')
  loop = asyncio.get_running_loop()
  print('try e: loop')
except RuntimeError as e:
  print(f'RuntimeError: {e}')
  print('except s: loop')
  lloop = RubiconEventLoop()
  #asyncio.set_event_loop(loop)
  print('except e: loop')

loop.run_forever()
loop.stop()
loop.close()
'''
