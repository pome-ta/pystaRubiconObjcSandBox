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

from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super

from objc_frameworks.Foundation import NSStringFromClass

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- Metal
from pyrubicon.objc.api import NSArray
from pyrubicon.objc.types import CGSize

from objc_frameworks.CoreGraphics import CGRectZero
from objc_frameworks.Metal import (
  MTLCreateSystemDefaultDevice,
  MTLClearColorMake,
  MTLResourceOptions,
  MTLPixelFormat,
  MTLPrimitiveType,
  MTLIndexType,
  MTLGPUFamily,
)

MTKView = ObjCClass('MTKView')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

shader_path = Path(Path(__file__).parent, 'Shader.metal')

shader_source = '''#include <metal_stdlib>
using namespace metal;


vertex float4 vertex_shader(const device packed_float3 *vertices [[ buffer(0) ]],
                            uint vertexId [[ vertex_id ]]) {
  return float4(vertices[vertexId], 1);
}

fragment half4 fragment_shader() {
  return half4(1, 0, 0, 1);
}
'''
#shader_code = shader_path.read_text('utf-8')


class Colors:
  wenderlichGreen = MTLClearColorMake(0.0, 0.4, 0.21, 1.0)


VertexArrayType = (ctypes.c_float * (3 * 3))


class MainViewController(UIViewController):

  metalView: MTKView = objc_property()
  commandQueue: 'MTLCommandQueue' = objc_property()
  vertices: '[Float]' = objc_property(object)
  pipelineState: 'MTLRenderPipelineState?' = objc_property()
  vertexBuffer: 'MTLBuffer?' = objc_property()

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
    self.navigationItem.title = NSStringFromClass(__class__)

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
    '''
    vertices = (ctypes.c_float * (3 * 3))(
       0.0,  1.0,  0.0,  # 1
      -1.0, -1.0,  0.0,  # 2
       1.0, -1.0,  0.0,  # 3
    )  # yapf: disable
    '''
    vertices = VertexArrayType(
       0.0,  1.0,  0.0,  # 1
      -1.0, -1.0,  0.0,  # 2
       1.0, -1.0,  0.0,  # 3
    )  # yapf: disable

    self.vertices = vertices
    self.buildModel()
    self.buildPipelineState()
    metalView.delegate = self

  # --- private
  @objc_method
  def buildModel(self):

    vertexBuffer = self.metalView.device.newBufferWithBytes_length_options_(
      self.vertices, ctypes.sizeof(self.vertices),
      MTLResourceOptions.storageModeShared)

    self.vertexBuffer = vertexBuffer

  @objc_method
  def buildPipelineState(self):
    source = shader_path.read_text('utf-8')
    #source = shader_source
    #source = shader_code
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
    print(f'    - {NSStringFromClass(__class__)}: viewWillAppear_')
    #self.metalView.enableSetNeedsDisplay = False
    #self.metalView.delegate = self
    #self.metalView.setPaused_(False)

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
    print(f'    - {NSStringFromClass(__class__)}: viewDidAppear_')

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])
    print(f'    - {NSStringFromClass(__class__)}: viewWillDisappear_')
    #self.metalView.setPaused_(True)

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

    print(f'    - {NSStringFromClass(__class__)}: viewDidDisappear_')

  @objc_method
  def didReceiveMemoryWarning(self):
    send_super(__class__, self, 'didReceiveMemoryWarning')
    print(f'	{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  # --- MTKViewDelegate
  @objc_method
  def mtkView_drawableSizeWillChange_(self, view, size: CGSize):
    print('      - mtkView_drawableSizeWillChange_')

  @objc_method
  def drawInMTKView_(self, view):
    print('d')
    if not ((drawable := view.currentDrawable) and
            (pipelineState := self.pipelineState) and
            (descriptor := view.currentRenderPassDescriptor)):
      return

    commandBuffer = self.commandQueue.commandBuffer()

    commandEncoder = commandBuffer.renderCommandEncoderWithDescriptor_(
      descriptor)
    commandEncoder.setRenderPipelineState_(pipelineState)
    commandEncoder.setVertexBuffer_offset_atIndex_(self.vertexBuffer, 0, 0)
    commandEncoder.drawPrimitives_vertexStart_vertexCount_(
      MTLPrimitiveType.triangle, 0, self.vertices.__len__())

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

