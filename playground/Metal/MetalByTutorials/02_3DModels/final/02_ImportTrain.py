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

from pyrubicon.objc.api import ObjCClass, ObjCProtocol
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super
from pyrubicon.objc.types import CGSize, CGRectMake

from objc_frameworks.Foundation import NSStringFromClass
from objc_frameworks.CoreGraphics import CGRectZero
from objc_frameworks.Metal import (
  MTLCreateSystemDefaultDevice,
  MTLClearColorMake,
  MTLVertexFormat,
  MTLPixelFormat,
  MTLPrimitiveType,
  MTLTriangleFillMode,
)
from objc_frameworks.MetalKit import (
  MTKMetalVertexDescriptorFromModelIO,
  MTKModelIOVertexDescriptorFromMetal,
)

from objc_frameworks.ModelIO import MDLVertexAttributePosition

from rbedge.utils import nsurl, get_str_filepath
from rbedge.simd import simd_float3

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')

MTKViewDelegate = ObjCProtocol('MTKViewDelegate')

MTKView = ObjCClass('MTKView')
MTKMeshBufferAllocator = ObjCClass('MTKMeshBufferAllocator')
MDLMesh = ObjCClass('MDLMesh')
MTLVertexDescriptor = ObjCClass('MTLVertexDescriptor')

MTKMesh = ObjCClass('MTKMesh')
MDLAsset = ObjCClass('MDLAsset')
MTLCompileOptions = ObjCClass('MTLCompileOptions')
MTLRenderPipelineDescriptor = ObjCClass('MTLRenderPipelineDescriptor')

shaders = '''
#include <metal_stdlib>
using namespace metal;

struct VertexIn {
  float4 position [[attribute(0)]];
};

vertex float4 vertex_main(const VertexIn vertex_in [[stage_in]]) {
float4 position = vertex_in.position;
position.y -= 1.0;
return position;
}

fragment float4 fragment_main() {
  return float4(1, 0, 0, 1);
}
'''


# wip: 雑
def _get_filepath(file_name: str) -> str | None:
  root = ROOT_PATH.parents[0] / 'resources'
  return get_str_filepath(root, file_name)


def get_model_path(
  modelName: str,
  extension: str = '',
) -> str | None:
  return _get_filepath(f'{modelName}.{extension}')


ROOT_PATH = Path(__file__).parents[0]


class MainViewController(UIViewController, protocols=[MTKViewDelegate]):

  metalView: MTKView = objc_property()
  mesh: MTKMesh = objc_property()
  commandQueue: 'MTLCommandQueue' = objc_property()
  pipelineState: 'MTLRenderPipelineState' = objc_property()

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'	 - {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.navigationItem.title = NSStringFromClass(__class__)
    self.navigationItem.subtitle = '2 Import Train'

    if (device := MTLCreateSystemDefaultDevice()) is None:
      raise ('GPU is not supported')

    # todo: `translatesAutoresizingMaskIntoConstraints = False` するので、レイアウトでサイズ調整
    #frame = CGRectMake(x=0, y=0, w=500, h=500)
    frame = CGRectZero

    metalView = MTKView.alloc().initWithFrame_device_(frame, device)
    metalView.clearColor = MTLClearColorMake(
      red=1,
      green=1,
      blue=0.8,
      alpha=1,
    )

    allocator = MTKMeshBufferAllocator.alloc().initWithDevice_(device)

    if not (assetURL := get_model_path('train', 'usdz')):
      raise ValueError('Asset `train` does not exist.')

    vertexDescriptor = MTLVertexDescriptor.new()
    vertexDescriptor.attributes.objectAtIndexedSubscript_(
      0).format = MTLVertexFormat.float3
    vertexDescriptor.attributes.objectAtIndexedSubscript_(0).offset = 0
    vertexDescriptor.attributes.objectAtIndexedSubscript_(0).bufferIndex = 0

    vertexDescriptor.layouts.objectAtIndexedSubscript_(
      0).stride = simd_float3.stride

    meshDescriptor = MTKModelIOVertexDescriptorFromMetal(vertexDescriptor)
    meshDescriptor.attributes.objectAtIndexedSubscript_(
      0).name = MDLVertexAttributePosition

    asset = MDLAsset.alloc().initWithURL(
      nsurl(assetURL),
      vertexDescriptor=meshDescriptor,
      bufferAllocator=allocator,
    )

    if not isinstance(
      (mdlMesh := asset.childObjectsOfClass_(MDLMesh).firstObject()), MDLMesh):
      raise TypeError(f'{mdlMesh}')

    try:
      mesh = MTKMesh.alloc().initWithMesh(
        mdlMesh,
        device=device,
        error=None,
      )
    except Exception as e:
      print(f'{e}')

    commandQueue = device.newCommandQueue()

    library = device.newLibraryWithSource_options_error_(
      shaders,
      MTLCompileOptions.new(),
      None,
    )
    vertexFunction = library.newFunctionWithName_('vertex_main')
    fragmentFunction = library.newFunctionWithName_('fragment_main')

    pipelineDescriptor = MTLRenderPipelineDescriptor.new()
    pipelineDescriptor.colorAttachments.objectAtIndexedSubscript_(
      0).pixelFormat = MTLPixelFormat.bgra8Unorm

    pipelineDescriptor.vertexFunction = vertexFunction
    pipelineDescriptor.fragmentFunction = fragmentFunction

    pipelineDescriptor.vertexDescriptor = MTKMetalVertexDescriptorFromModelIO(
      mesh.vertexDescriptor)

    try:
      pipelineState = device.newRenderPipelineStateWithDescriptor_error_(
        pipelineDescriptor, None)
    except Exception as e:
      print(f'{e}')

    metalView.delegate = self

    metalView.enableSetNeedsDisplay = True
    metalView.setNeedsDisplay()

    self.view.addSubview_(metalView)

    self.metalView = metalView
    self.mesh = mesh
    self.commandQueue = commandQueue
    self.pipelineState = pipelineState

    self.setupLayoutConstraint()

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

  @objc_method
  def viewDidAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

  @objc_method
  def viewWillDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

  @objc_method
  def viewDidDisappear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewDidDisappear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

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
    if not ((commandBuffer := self.commandQueue.commandBuffer()) and
            (renderPassDescriptor := view.currentRenderPassDescriptor) and
            (renderEncoder := commandBuffer.
             renderCommandEncoderWithDescriptor_(renderPassDescriptor))):
      return

    renderEncoder.setRenderPipelineState_(self.pipelineState)

    renderEncoder.setVertexBuffer(
      self.mesh.vertexBuffers.objectAtIndexedSubscript_(0).buffer,
      offset=0,
      atIndex=0,
    )

    renderEncoder.setTriangleFillMode_(MTLTriangleFillMode.lines)

    for submesh in self.mesh.submeshes:
      renderEncoder.drawIndexedPrimitives(
        MTLPrimitiveType.triangle,
        indexCount=submesh.indexCount,
        indexType=submesh.indexType,
        indexBuffer=submesh.indexBuffer.buffer,
        indexBufferOffset=0,
      )

    renderEncoder.endEncoding()
    if not (drawable := view.currentDrawable):
      return
    commandBuffer.presentDrawable_(drawable)
    commandBuffer.commit()

  # --- private
  @objc_method
  def setupLayoutConstraint(self):
    from objc_frameworks.UIKit import UILayoutPriorityDefaultHigh
    NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

    self.metalView.translatesAutoresizingMaskIntoConstraints = False

    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    # センター
    centerXAnchor = self.metalView.centerXAnchor.constraintEqualToAnchor_(
      safeAreaLayoutGuide.centerXAnchor)
    centerYAnchor = self.metalView.centerYAnchor.constraintEqualToAnchor_(
      safeAreaLayoutGuide.centerYAnchor)

    # 固定サイズ(500)
    fixedWidth = self.metalView.widthAnchor.constraintEqualToConstant_(500)
    fixedWidth.setPriority_(UILayoutPriorityDefaultHigh)
    fixedHeight = self.metalView.heightAnchor.constraintEqualToConstant_(500)
    fixedHeight.setPriority_(UILayoutPriorityDefaultHigh)

    # safeArea に対する88%
    maxWidth = self.metalView.widthAnchor.constraintLessThanOrEqualToAnchor_multiplier_(
      safeAreaLayoutGuide.widthAnchor,
      0.88,
    )
    maxHeight = self.metalView.heightAnchor.constraintLessThanOrEqualToAnchor_multiplier_(
      safeAreaLayoutGuide.heightAnchor,
      0.88,
    )

    # スクエア定義
    aspect = self.metalView.widthAnchor.constraintEqualToAnchor_(
      self.metalView.heightAnchor)

    NSLayoutConstraint.activateConstraints_([
      centerXAnchor,
      centerYAnchor,
      fixedWidth,
      fixedHeight,
      maxWidth,
      maxHeight,
      aspect,
    ])


if __name__ == '__main__':
  from rbedge.app import App
  from objc_frameworks.UIKit import UIModalPresentationStyle

  main_vc = MainViewController.new()

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()

