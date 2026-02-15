'''
import asyncio
from pyrubicon.objc.eventloop import RubiconEventLoop, EventLoopPolicy

__all__ = [
  'loop',
]

try:
  print('try s: loop')
  loop = asyncio.get_running_loop()
  print('try e: loop')
except RuntimeError as e:
  print(f'RuntimeError: {e}')
  print('except s: loop')
  loop = RubiconEventLoop()
  asyncio.set_event_loop(loop)
  print('except e: loop')

# loop.set_debug(True)
'''
'''
import asyncio
from pyrubicon.objc.eventloop import RubiconEventLoop, EventLoopPolicy

__all__ = [
  'loop',
]

print('try s: loop')
loop = RubiconEventLoop()
asyncio.set_event_loop(loop)
print('try e: loop')
'''
'''
try:
  print('try s: loop')
  loop = asyncio.get_running_loop()
  print('try e: loop')
except RuntimeError as e:
  print(f'RuntimeError: {e}')
  print('except s: loop')
  loop = RubiconEventLoop()
  asyncio.set_event_loop(loop)
  print('except e: loop')

# loop.set_debug(True)
'''

import asyncio
#import logging

from pyrubicon.objc.eventloop import EventLoopPolicy

__all__ = [
  'loop',
]

# wip: asyncio
#logging.basicConfig(level=logging.DEBUG)
print('flat s: loop')
asyncio.set_event_loop_policy(EventLoopPolicy())
#loop = asyncio.get_event_loop()
loop = asyncio.new_event_loop()
#loop.set_debug(True)
print('flat e: loop')

