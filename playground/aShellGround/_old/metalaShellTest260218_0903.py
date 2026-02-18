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

from pyrubicon.objc.api import Block, ObjCInstance, ObjCProtocol
from pyrubicon.objc.runtime import autoreleasepool, objc_id, load_library, SEL
from pyrubicon.objc.types import CGSize

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

from rbedge.objcMainThread import onMainThread

#Metal = load_library('Metal')
#MetalKit = load_library('MetalKit')

MTKView = ObjCClass('MTKView')

MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

#MTKViewDelegate = ObjCProtocol('MTKViewDelegate')

shader_path = Path('./Shader.metal')


class Colors:
  wenderlichGreen = MTLClearColorMake(0.0, 0.4, 0.21, 1.0)


class Constants(ctypes.Structure):
  _fields_ = [
    ('animateBy', ctypes.c_float),
  ]


#class MainViewController(UIViewController, protocols=[MTKViewDelegate]):
class MainViewController(UIViewController):
  metalView: MTKView = objc_property()
  commandQueue: 'MTLCommandQueue' = objc_property()
  device: 'MTLCreateSystemDefaultDevice' = objc_property(weak=True)
  vertices: '[Float]'
  indices: '[UInt16]'
  pipelineState: 'MTLRenderPipelineState?'
  vertexBuffer: 'MTLBuffer?'
  indexBuffer: 'MTLBuffer?'
  constants: Constants
  time: float
  semaphore: ObjCInstance

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    print(f'	 - {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    print(f'    - {NSStringFromClass(__class__)}: loadView')

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    print(f'    - {NSStringFromClass(__class__)}: viewDidLoad')
    #self.navigationItem.title = NSStringFromClass(__class__)
    self.performSelectorOnMainThread_withObject_waitUntilDone_(
      SEL('metalViewDidLoad:'), None, True)
    #pdbr.state(self)

  #@onMainThread  #(sync=False)
  @objc_method
  def metalViewDidLoad_(self, dmy):

    #self.navigationItem.title = NSStringFromClass(__class__)

    device = MTLCreateSystemDefaultDevice()

    metalView = MTKView.alloc().initWithFrame_device_(CGRectZero, device)
    metalView.clearColor = Colors.wenderlichGreen

    #metalView.delegate = self
    commandQueue = device.newCommandQueue()

    #metalView.setPaused_(True)
    #metalView.enableSetNeedsDisplay = True
    #metalView.setNeedsDisplay()

    self.view.addSubview_(metalView)

    # --- Layout
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    metalView.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      metalView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      metalView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      metalView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor, 0.5),
      metalView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor, 0.5),
    ])

    self.metalView = metalView
    self.commandQueue = commandQueue
    self.device = device
    #self.semaphore = dispatch_semaphore_create(3)

    self.renderer()

  #@onMainThread(sync=False)
  @objc_method
  def renderer(self):
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
    '''

    vertexBuffer = self.device.newBufferWithBytes_length_options_(
      self.vertices, ctypes.sizeof(self.vertices), 0)
    indexBuffer = self.device.newBufferWithBytes_length_options_(
      self.indices, ctypes.sizeof(self.indices), 0)
    self.vertexBuffer = vertexBuffer
    self.indexBuffer = indexBuffer
    '''

  @objc_method
  def buildPipelineState(self):
    source = shader_path.read_text('utf-8')
    options = MTLCompileOptions.new()

    library = self.device.newLibraryWithSource_options_error_(
      source, None, None)

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

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'    - {NSStringFromClass(__class__)}: viewWillAppear_')
    self.navigationItem.title = NSStringFromClass(__class__)
    self.metalView.delegate = self

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #self.metalView.setPaused_(False)

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #self.metalView.setPaused_(True)
    print(f'    - {NSStringFromClass(__class__)}: viewWillDisappear_')

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    #self.metalView = None
    #self.metalView.device = None
    #pdbr.state(self.metalView)
    print(f'    - {NSStringFromClass(__class__)}: viewDidDisappear_')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'	{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  # --- MTKViewDelegate
  @objc_method
  def mtkView_drawableSizeWillChange_(self, view, size: CGSize):
    pass

  @objc_method
  def drawInMTKView_(self, view):
    print('d')
    #dispatch_semaphore_wait(self.semaphore, DISPATCH_TIME_FOREVER)

    with autoreleasepool():
      if not ((drawable := view.currentDrawable) and
              (pipelineState := self.pipelineState) and
              (indexBuffer := self.indexBuffer) and
              (descriptor := view.currentRenderPassDescriptor)):
        #dispatch_semaphore_signal(self.semaphore)

        return
      commandBuffer = self.commandQueue.commandBuffer()
      
      def completion_handler(buffer):
        dispatch_semaphore_signal(self.semaphore)

      # Block(関数, 戻り値, 引数...)
      handler_block = Block(completion_handler, None, objc_id)
      #commandBuffer.addCompletedHandler_(handler_block)

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
  from rbedge.app import App
  from objc_frameworks.UIKit import UIModalPresentationStyle

  print('--- --- start')
  main_vc = MainViewController.new()

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  print('main')
  app.present()
  print('main.present')
  print('### ### ###')

