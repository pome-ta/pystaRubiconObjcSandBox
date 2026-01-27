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

from rbedge import pdbr

UIViewController = ObjCClass('UIViewController')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

CIImage = ObjCClass('CIImage')

#pdbr.state(CIImage)

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

    debugOptions = showFeaturePoints | showWorldOrigin
    arscnView.debugOptions = debugOptions
    arscnView.showsStatistics = True

    self.view.addSubview_(arscnView)

    # --- Layout
    arscnView.translatesAutoresizingMaskIntoConstraints = False

    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

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

    self.arscnView = arscnView

  @objc_method
  def viewWillAppear_(self, animated: bool):
    send_super(__class__,
               self,
               'viewWillAppear:',
               animated,
               argtypes=[
                 ctypes.c_bool,
               ])

    configuration = ARWorldTrackingConfiguration.new()
    configuration.environmentTexturing = AREnvironmentTexturing.automatic

    frameSemantics = ARFrameSemantics.sceneDepth
    if ARWorldTrackingConfiguration.supportsFrameSemantics_(frameSemantics):
      configuration.frameSemantics = frameSemantics

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
    #print('didUpdateFrame')
    #pdbr.state(session.currentFrame.sceneDepth.depthMap)
    #print(session.currentFrame)
    if not (pixelBuffer := session.currentFrame.sceneDepth.depthMap):
      return 
    #print(pixelBuffer())
    #print('')
    #ciImage = CIImage.alloc().initWithCVPixelBuffer_(pixelBuffer)
    ciImage = CIImage.imageWithCVPixelBuffer_(pixelBuffer)
    #imageWithCVPixelBuffer_
    #print(ciImage)
    print(ciImage.debugDescription)
    #print('__')
    
    
    #pdbr.state(session.currentFrame.sceneDepth.depthMap)
    #print(pixelBuffer)
    #print(session.currentFrame)
    pass

'''
extension ARFrame {
    func depthMapTransformedImage(orientation: UIInterfaceOrientation, viewPort: CGRect) -> UIImage? {
        guard let pixelBuffer = self.sceneDepth?.depthMap else { return nil }
        let ciImage = CIImage(cvPixelBuffer: pixelBuffer)
        return UIImage(ciImage: screenTransformed(ciImage: ciImage, orientation: orientation, viewPort: viewPort))
    }
'''



if __name__ == '__main__':
  from rbedge.app import App
  from objc_frameworks.UIKit import UIModalPresentationStyle

  main_vc = DepthMapViewController.new()

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()

