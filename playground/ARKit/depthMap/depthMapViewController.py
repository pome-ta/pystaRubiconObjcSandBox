# [ExampleOfiOSLiDAR/ExampleOfiOSLiDAR/Samples/Depth/DepthMapViewController.swift at main · TokyoYoshida/ExampleOfiOSLiDAR · GitHub](https://github.com/TokyoYoshida/ExampleOfiOSLiDAR/blob/main/ExampleOfiOSLiDAR/Samples/Depth/DepthMapViewController.swift)
_TOP_DIR_NAME = 'pystaRubiconObjcSandBox'
_MODULES_DIR_NAME = 'modules'

# todo: `./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME}` にあるpackage のimport 準備
if __name__ == '__main__' and not __file__[:__file__.rfind('/')].endswith(
    _TOP_DIR_NAME):
  import pathlib
  import sys
  __parents = pathlib.Path(__file__).resolve().parents
  for path in __parents:
    if path.name == _TOP_DIR_NAME and (__modules_path :=
                                       path / _MODULES_DIR_NAME).exists():
      sys.path.insert(0, str(__modules_path))
      break
  else:
    import warnings
    with warnings.catch_warnings():
      warnings.simplefilter('always', ImportWarning)
      __warning_message = f'./{_TOP_DIR_NAME}/{_MODULES_DIR_NAME} not found in parent directories'
      warnings.warn(__warning_message, ImportWarning)

import ctypes

from pyrubicon.objc.api import ObjCClass
from pyrubicon.objc.api import objc_method, objc_property
from pyrubicon.objc.runtime import send_super

from objc_frameworks.Foundation import NSStringFromClass
from objc_frameworks.CoreGraphics import CGRectZero
from objc_frameworks.CoreGraphics import (
  CGAffineTransformIdentity,
  CGAffineTransformMakeScale,
  CGAffineTransformTranslate,
  CGAffineTransformConcat,
)
from objc_frameworks.UIKit import UIInterfaceOrientation

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

UIApplication = ObjCClass('UIApplication')
CIImage = ObjCClass('CIImage')
CIContext = ObjCClass('CIContext')
UIImage = ObjCClass('UIImage')
UIImageView = ObjCClass('UIImageView')

# --- SceneKit
from objc_frameworks.SceneKit import (
  SCNPreferredRenderingAPIKey,
  SCNRenderingAPI,
  SCNDebugOptions,
)

# --- ARKit
from objc_frameworks.ARKit import (
  showFeaturePoints,
  showWorldOrigin,
  ARFrameSemantics,
  AREnvironmentTexturing,
)

ARSCNView = ObjCClass('ARSCNView')
ARWorldTrackingConfiguration = ObjCClass('ARWorldTrackingConfiguration')


class DepthMapViewController(UIViewController):

  arscnView: ARSCNView = objc_property()
  imageView: UIImageView = objc_property()
  orientation: int  # = objc_property()

  framePick: bool  # = objc_property()

  @objc_method
  def dealloc(self):
    # xxx: 呼ばない-> `send_super(__class__, self, 'dealloc')`
    #print(f'\t - {NSStringFromClass(__class__)}: dealloc')
    pass

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')
    self.navigationItem.title = NSStringFromClass(__class__)

    arscnView = ARSCNView.alloc().initWithFrame_options_(
      CGRectZero, {
        SCNPreferredRenderingAPIKey: SCNRenderingAPI.metal,
      })

    debugOptions = showFeaturePoints  #| showWorldOrigin
    arscnView.debugOptions = debugOptions
    arscnView.showsStatistics = True

    imageView = UIImageView.new()

    self.view.addSubview_(arscnView)
    self.view.addSubview_(imageView)

    # --- Layout
    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    arscnView.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      arscnView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      arscnView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      arscnView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor, 1.0),
      arscnView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor, 1.0),
    ])

    imageView.translatesAutoresizingMaskIntoConstraints = False
    NSLayoutConstraint.activateConstraints_([
      imageView.leadingAnchor.constraintEqualToAnchor_constant_(
        self.view.leadingAnchor, 50.0),
      imageView.trailingAnchor.constraintEqualToAnchor_constant_(
        self.view.trailingAnchor, -50.0),
      imageView.heightAnchor.constraintEqualToConstant_(700.0),  # 定数
      imageView.centerYAnchor.constraintEqualToAnchor_(
        self.view.centerYAnchor),
    ])

    self.arscnView = arscnView
    self.imageView = imageView
    self.framePick = False

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

    # wip: 評価して出す。いまは固定

    if not isinstance(
        orientation := UIApplication.sharedApplication.windows[0].windowScene.
        interfaceOrientation, int):
      raise TypeError(f'expected int, got {type(orientation).__name__}')

    configuration = ARWorldTrackingConfiguration.new()
    configuration.environmentTexturing = AREnvironmentTexturing.automatic

    frameSemantics = ARFrameSemantics.sceneDepth
    if ARWorldTrackingConfiguration.supportsFrameSemantics_(frameSemantics):
      configuration.frameSemantics = frameSemantics

    self.orientation = orientation
    self.arscnView.session.delegate = self
    self.arscnView.session.runWithConfiguration_(configuration)

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
    self.arscnView.session.pause()

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
    print(f'\t{NSStringFromClass(__class__)}: didReceiveMemoryWarning')

  # MARK: - ARSessionDelegate
  @objc_method
  def session_didUpdateFrame_(self, session, frame):
    # --- func depthMapTransformedImage(orientation: UIInterfaceOrientation, viewPort: CGRect) -> UIImage?
    '''
    if not (pixelBuffer := session.currentFrame.sceneDepth.depthMap):
      return
    '''
    if not (pixelBuffer := frame.sceneDepth.depthMap):
      return
    ciImage = CIImage.alloc().initWithCVPixelBuffer_(pixelBuffer)
    viewPort = self.imageView.bounds
    # --- func screenTransformed(ciImage: CIImage, orientation: UIInterfaceOrientation, viewPort: CGRect)

    viewPortSize = viewPort.size
    captureSize = ciImage.extent.size
    # --- func screenTransform(orientation: UIInterfaceOrientation, viewPortSize: CGSize, captureSize: CGSize)
    if self.framePick:
      return
    self.framePick = True
    #height
    #width

    normalizeTransform = CGAffineTransformMakeScale(1.0 / captureSize.width,
                                                    1.0 / captureSize.height)
    flipTransform = CGAffineTransformTranslate(
      CGAffineTransformMakeScale(-1.0, -1.0), -1.0, -1.0
    ) if UIInterfaceOrientation.portrait == self.orientation else CGAffineTransformIdentity

    #print(normalizeTransform)

    #displayTransformForOrientation_viewportSize_

    displayTransform = frame.displayTransformForOrientation_viewportSize_(
      self.orientation, viewPortSize)

    #pdbr.state(displayTransform)
    print(displayTransform)

    cgImage = CIContext.new().createCGImage_fromRect_(ciImage, ciImage.extent)
    uiImage = UIImage.imageWithCGImage_(cgImage)

    #self.imageView.image = uiImage


if __name__ == '__main__':
  from rbedge.app import App
  from objc_frameworks.UIKit import UIModalPresentationStyle

  main_vc = DepthMapViewController.new()

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()

