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
from pathlib import Path
from math import sin

from pyrubicon.objc.api import ObjCClass, NSObject
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSize, CGFloat

from rbedge import pdbr

from objc_frameworks.Metal import (
  MTLResourceOptions,
  MTLPixelFormat,
  MTLPrimitiveType,
  MTLIndexType,
)

MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

shader_path = Path(__file__).parent / 'Shader.metal'


class Constants(ctypes.Structure):
  _fields_ = [
    ('animateBy', ctypes.c_float),
  ]


class Renderer(NSObject):

  device: 'MTLDevice' = objc_property()
  commandQueue: 'MTLCommandQueue' = objc_property()
  vertices: '[Float]' = objc_property(object)
  indices: '[UInt16]' = objc_property(object)
  pipelineState: 'MTLRenderPipelineState?' = objc_property()
  vertexBuffer: 'MTLBuffer?' = objc_property()
  indexBuffer: 'MTLBuffer?' = objc_property()
  constants: Constants = objc_property(object)
  time: CGFloat = objc_property(CGFloat)

  @objc_method
  def initWithDevice_(self, device):
    send_super(__class__, self, 'init')
    self.device = device
    self.commandQueue = device.newCommandQueue()
    self.vertices = (ctypes.c_float * (4 * 3))(
      -1.0,  1.0,  0.0,  # v0
      -1.0, -1.0,  0.0,  # v1
       1.0, -1.0,  0.0,  # v2
       1.0,  1.0,  0.0,  # v3
    )  # yapf: disable
    self.indices = (ctypes.c_int16 * (2 * 3))(
      0, 1, 2,
      2, 3, 0,
    )  # yapf: disable
    self.constants = Constants()
    self.time = 0.0

    self.buildModel()
    self.buildPipelineState()

    return self

  # --- private
  @objc_method
  def buildModel(self):
    vertexBuffer = self.device.newBufferWithBytes_length_options_(
      self.vertices, ctypes.sizeof(self.vertices),
      MTLResourceOptions.storageModeShared)
    indexBuffer = self.device.newBufferWithBytes_length_options_(
      self.indices, ctypes.sizeof(self.indices),
      MTLResourceOptions.storageModeShared)

    self.vertexBuffer = vertexBuffer
    self.indexBuffer = indexBuffer

  @objc_method
  def buildPipelineState(self):
    source = shader_path.read_text('utf-8')
    options = MTLCompileOptions.new()

    library = self.device.newLibraryWithSource_options_error_(
      source, options, None)

    vertexFunction = library.newFunctionWithName_('vertex_shader')
    fragmentFunction = library.newFunctionWithName_('fragment_shader')

    pipelineDescriptor = MTLRenderPipelineDescriptor.new()
    pipelineDescriptor.vertexFunction = vertexFunction
    pipelineDescriptor.fragmentFunction = fragmentFunction
    pipelineDescriptor.colorAttachments.objectAtIndexedSubscript_(
      0).pixelFormat = MTLPixelFormat.bgra8Unorm

    pipelineState = None
    try:
      pipelineState = self.device.newRenderPipelineStateWithDescriptor_error_(
        pipelineDescriptor, None)
    except Exception as e:
      print(f'pipelineState error: {e}')

    self.pipelineState = pipelineState

  # --- MTKViewDelegate
  @objc_method
  def mtkView_drawableSizeWillChange_(self, view, size: CGSize):
    pass

  @objc_method
  def drawInMTKView_(self, view):
    if not ((drawable := view.currentDrawable) and
            (pipelineState := self.pipelineState) and
            (indexBuffer := self.indexBuffer) and
            (descriptor := view.currentRenderPassDescriptor)):
      return

    self.time += 1 / view.preferredFramesPerSecond
    animateBy = abs(sin(self.time) / 2 + 0.5)
    self.constants.animateBy = animateBy

    commandBuffer = self.commandQueue.commandBuffer()

    commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
      descriptor)
    commandEncoder.setRenderPipelineState_(pipelineState)
    commandEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
    commandEncoder.setVertexBytes_length_atIndex_(
      ctypes.byref(self.constants), ctypes.sizeof(self.constants), 1)

    commandEncoder.drawIndexedPrimitives_indexCount_indexType_indexBuffer_indexBufferOffset_(
      MTLPrimitiveType.triangle, self.indices.__len__(), MTLIndexType.uInt16,
      self.indexBuffer, 0)

    commandEncoder.endEncoding()
    commandBuffer.presentDrawable_(drawable)
    commandBuffer.commit()


if __name__ == '__main__':
  from objc_frameworks.Metal import MTLCreateSystemDefaultDevice

  renderer = Renderer.alloc().initWithDevice_(MTLCreateSystemDefaultDevice())

