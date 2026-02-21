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

from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super

from objc_frameworks.Foundation import NSStringFromClass

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- Metal
from pyrubicon.objc.api import Block
from pyrubicon.objc.runtime import autoreleasepool, objc_block, objc_id
from pyrubicon.objc.types import CGSize, CGFloat

from objc_frameworks.CoreGraphics import CGRectZero
from objc_frameworks.Metal import (
  MTLCreateSystemDefaultDevice,
  MTLClearColorMake,
  MTLResourceOptions,
  MTLPixelFormat,
  MTLPrimitiveType,
  MTLIndexType,
)

from objc_frameworks.Dispatch import (
  dispatch_semaphore_create,
  dispatch_semaphore_wait,
  dispatch_semaphore_signal,
  DISPATCH_TIME_FOREVER,
)

MTKView = ObjCClass('MTKView')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

shader_path = Path(__file__).parent / 'Shader.metal'


class Colors:
  wenderlichGreen = MTLClearColorMake(0.0, 0.4, 0.21, 1.0)


class Constants(ctypes.Structure):
  _fields_ = [
    ('animateBy', ctypes.c_float),
  ]


class MainViewController(UIViewController):

  metalView: MTKView = objc_property()
  commandQueue: 'MTLCommandQueue' = objc_property()
  vertices: '[Float]' = objc_property(object)
  indices: '[UInt16]' = objc_property(object)
  pipelineState: 'MTLRenderPipelineState?' = objc_property()
  vertexBuffer: 'MTLBuffer?' = objc_property()
  indexBuffer: 'MTLBuffer?' = objc_property()
  constants: Constants = objc_property(object)
  time: float = objc_property(CGFloat)
  semaphore: 'dispatch_semaphore_t' = objc_property()

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'	 - {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    #print(f'    - {NSStringFromClass(__class__)}: loadView')

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    #print(f'    - {NSStringFromClass(__class__)}: viewDidLoad')
    self.navigationItem.title = NSStringFromClass(__class__)

    device = MTLCreateSystemDefaultDevice()
    metalView = MTKView.alloc().initWithFrame_device_(CGRectZero, device)
    metalView.clearColor = Colors.wenderlichGreen

    commandQueue = device.newCommandQueue()

    metalView.delegate = self

    #metalView.setPaused_(True)
    #metalView.enableSetNeedsDisplay = True
    #metalView.setNeedsDisplay()

    self.view.addSubview_(metalView)

    self.metalView = metalView
    self.commandQueue = commandQueue
    self.semaphore = dispatch_semaphore_create(3)

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

    self.setupLayoutConstraint()

  # --- private
  @objc_method
  def setupLayoutConstraint(self):
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    self.metalView.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      self.metalView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      self.metalView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      self.metalView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor, 0.5),
      self.metalView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor, 0.5),
    ])

  @objc_method
  def buildModel(self):

    vertexBuffer = self.metalView.device.newBufferWithBytes_length_options_(
      self.vertices, ctypes.sizeof(self.vertices),
      MTLResourceOptions.storageModeShared)
    indexBuffer = self.metalView.device.newBufferWithBytes_length_options_(
      self.indices, ctypes.sizeof(self.indices),
      MTLResourceOptions.storageModeShared)

    self.vertexBuffer = vertexBuffer
    self.indexBuffer = indexBuffer

  @objc_method
  def buildPipelineState(self):
    source = shader_path.read_text('utf-8')
    options = MTLCompileOptions.new()

    library = self.metalView.device.newLibraryWithSource_options_error_(
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
      pipelineState = self.metalView.device.newRenderPipelineStateWithDescriptor_error_(
        pipelineDescriptor, None)
    except Exception as e:
      print(f'pipelineState error: {e}')

    self.pipelineState = pipelineState

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'    - {NSStringFromClass(__class__)}: viewWillAppear_')

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'    - {NSStringFromClass(__class__)}: viewDidAppear_')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'    - {NSStringFromClass(__class__)}: viewWillDisappear_')
    self.metalView.setPaused_(True)

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #print(f'    - {NSStringFromClass(__class__)}: viewDidDisappear_')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'	{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  # --- MTKViewDelegate
  @objc_method
  def mtkView_drawableSizeWillChange_(self, view, size: CGSize):
    #print('      - mtkView_drawableSizeWillChange_')
    pass

  @objc_method
  def drawInMTKView_(self, view):
    dispatch_semaphore_wait(self.semaphore, DISPATCH_TIME_FOREVER)

    with autoreleasepool():
      if not ((drawable := view.currentDrawable) and
              (pipelineState := self.pipelineState) and
              (indexBuffer := self.indexBuffer) and
              (descriptor := view.currentRenderPassDescriptor)):
        dispatch_semaphore_signal(self.semaphore)
        return

      self.time += 1 / view.preferredFramesPerSecond
      animateBy = abs(sin(self.time) / 2 + 0.5)
      self.constants.animateBy = animateBy

      commandBuffer = self.commandQueue.commandBuffer()

      def completion_handler(buffer):
        dispatch_semaphore_signal(self.semaphore)

      # Block(関数, 戻り値, 引数...)
      handler_block = Block(completion_handler, None, objc_id)
      commandBuffer.addCompletedHandler_(handler_block)

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
  from rbedge.app import App
  from objc_frameworks.UIKit import UIModalPresentationStyle

  main_vc = MainViewController.new()

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()

