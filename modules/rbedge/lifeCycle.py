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

