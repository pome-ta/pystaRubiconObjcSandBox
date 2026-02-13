'''

import asyncio
from pyrubicon.objc.eventloop import RubiconEventLoop, EventLoopPolicy

__all__ = [
  'loop',
]


try:
  loop = asyncio.get_running_loop()
except RuntimeError:
  loop = RubiconEventLoop()
  asyncio.set_event_loop(loop)


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
asyncio.set_event_loop_policy(EventLoopPolicy())
#loop = asyncio.get_event_loop()
loop = asyncio.new_event_loop()
#loop.set_debug(True)
