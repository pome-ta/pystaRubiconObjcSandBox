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

from pathlib import Path
from pyrubicon.objc.api import ObjCClass, ObjCInstance
from pyrubicon.objc.api import objc_const, NSDictionary
from pyrubicon.objc.runtime import load_library

from objc_frameworks.Metal import MTLCreateSystemDefaultDevice
from objc_frameworks.MetalKit import (
  MTKTextureLoaderOptionOrigin,
  MTKTextureLoaderOriginBottomLeft,
  MTKTextureLoaderOriginTopLeft,
)

from rbedge import pdbr
from rbedge.utils import nsurl

MTKTextureLoader = ObjCClass('MTKTextureLoader')

NSURL = ObjCClass('NSURL')
'''
def nsurl(url_or_path):
  if not isinstance(url_or_path, str):
    raise TypeError('expected a string')
  return NSURL.URLWithString_(
    url_or_path) if ':' in url_or_path else NSURL.fileURLWithPath_(url_or_path)
'''

device = MTLCreateSystemDefaultDevice()
textureLoader = MTKTextureLoader.alloc().initWithDevice_(device)

#origin = str(MTKTextureLoaderOriginBottomLeft)

origin = str(MTKTextureLoaderOriginTopLeft)
#textureLoaderOptions = {str(MTKTextureLoaderOptionOrigin): origin}
textureLoaderOptions = NSDictionary.dictionaryWithObject_forKey_(
  origin, MTKTextureLoaderOptionOrigin)

image_path = Path(
  '../Metal/BeginningMetal/06_Textures/final/Images/picture.png')  #.resolve()

path_str = str(image_path.resolve())

texture = textureLoader.newTextureWithContentsOfURL_options_error_(
  nsurl(path_str), textureLoaderOptions, None)

#pdbr.state(NSDictionary)
pdbr.state(texture)

if __name__ == '__main__':
  pass

