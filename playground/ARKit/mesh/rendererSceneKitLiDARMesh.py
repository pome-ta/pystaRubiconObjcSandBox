# [SceneKitLiDARMesh.swift](https://gist.github.com/eospi/b54e412afde3f07942240e0e306a32f2)

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
UIColor = ObjCClass('UIColor')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')

# --- SceneKit
from objc_frameworks.SceneKit import (
  SCNPreferredRenderingAPIKey,
  SCNRenderingAPI,
  SCNDebugOptions,
  SCNLightingModel,
  SCNFillMode,
  SCNGeometrySourceSemantic,
  SCNGeometryPrimitiveType,
)

SCNGeometrySource = ObjCClass('SCNGeometrySource')
SCNGeometryElement = ObjCClass('SCNGeometryElement')
SCNGeometry = ObjCClass('SCNGeometry')
SCNMaterial = ObjCClass('SCNMaterial')
SCNNode = ObjCClass('SCNNode')

# --- ARKit
from objc_frameworks.ARKit import (
  showFeaturePoints,
  showWorldOrigin,
  ARCoachingGoal,
  ARSceneReconstruction,
  ARFrameSemantics,
  AREnvironmentTexturing,
)

ARSCNView = ObjCClass('ARSCNView')
ARCoachingOverlayView = ObjCClass('ARCoachingOverlayView')
ARWorldTrackingConfiguration = ObjCClass('ARWorldTrackingConfiguration')
ARMeshAnchor = ObjCClass('ARMeshAnchor')


# xxx: 謎class になっちゃった、、、
class ARSCNMeshGeometry:

  scnGeometry: SCNGeometry
  __node: SCNNode

  def __init__(self, meshAnchor):
    meshGeometry = meshAnchor.geometry

    # Vertices source
    vertices = meshGeometry.vertices
    verticesSource = SCNGeometrySource.geometrySourceWithBuffer_vertexFormat_semantic_vertexCount_dataOffset_dataStride_(
      vertices.buffer, vertices.format, SCNGeometrySourceSemantic.vertex,
      vertices.count, vertices.offset, vertices.stride)

    # Indices Element
    faces = meshGeometry.faces
    facesElement = SCNGeometryElement.geometryElementWithBuffer_primitiveType_primitiveCount_bytesPerIndex_(
      faces.buffer, SCNGeometryPrimitiveType.triangles, faces.count,
      faces.bytesPerIndex)

    self.scnGeometry = SCNGeometry.geometryWithSources_elements_([
      verticesSource,
    ], [
      facesElement,
    ])

  @property
  def node(self) -> SCNNode:
    return self.__node

  def setNode_(self, material) -> SCNNode:
    scnMaterial = SCNMaterial.new()
    scnMaterial.diffuse.setContents_(material)

    geometry = self.scnGeometry
    geometry.setMaterials_([
      scnMaterial,
    ])

    self.__node = SCNNode.nodeWithGeometry_(geometry)
    return self.__node


class MainViewController(UIViewController):

  scnView: ARSCNView = objc_property()
  coachingOverlayView: ARCoachingOverlayView = objc_property()

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

    #scnView = ARSCNView.new()
    scnView = ARSCNView.alloc().initWithFrame_options_(
      CGRectZero, {
        SCNPreferredRenderingAPIKey: SCNRenderingAPI.metal,
      })

    # MARK: - ARSCNViewDelegate
    scnView.setDelegate_(self)

    debugOptions = showFeaturePoints | showWorldOrigin
    scnView.setDebugOptions_(debugOptions)
    scnView.setShowsStatistics_(True)

    coachingOverlayView = ARCoachingOverlayView.new()
    coachingOverlayView.setGoal_(ARCoachingGoal.tracking)
    coachingOverlayView.setActivatesAutomatically_(True)
    coachingOverlayView.setSession_(scnView.session)
    coachingOverlayView.setActive_animated_(True, True)

    scnView.addSubview_(coachingOverlayView)
    self.view.addSubview_(scnView)

    # --- Layout

    scnView.translatesAutoresizingMaskIntoConstraints = False
    coachingOverlayView.translatesAutoresizingMaskIntoConstraints = False

    safeAreaLayoutGuide = self.view.safeAreaLayoutGuide

    NSLayoutConstraint.activateConstraints_([
      scnView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      scnView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      scnView.widthAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.widthAnchor, 1.0),
      scnView.heightAnchor.constraintEqualToAnchor_multiplier_(
        safeAreaLayoutGuide.heightAnchor, 1.0),
    ])

    NSLayoutConstraint.activateConstraints_([
      coachingOverlayView.centerXAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerXAnchor),
      coachingOverlayView.centerYAnchor.constraintEqualToAnchor_(
        safeAreaLayoutGuide.centerYAnchor),
      coachingOverlayView.widthAnchor.constraintEqualToAnchor_multiplier_(
        scnView.widthAnchor, 1.0),
      coachingOverlayView.heightAnchor.constraintEqualToAnchor_multiplier_(
        scnView.heightAnchor, 1.0),
    ])

    self.scnView = scnView
    self.coachingOverlayView = coachingOverlayView

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

    sceneReconstruction = ARSceneReconstruction.meshWithClassification
    #sceneReconstruction = ARSceneReconstruction.mesh
    configuration.setSceneReconstruction_(sceneReconstruction)

    environmentTexturing = AREnvironmentTexturing.automatic
    configuration.setEnvironmentTexturing_(environmentTexturing)

    self.scnView.setAutomaticallyUpdatesLighting_(True)
    self.scnView.setAutoenablesDefaultLighting_(True)
    self.scnView.session.runWithConfiguration_(configuration)

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
    self.scnView.session.pause()

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

  # MARK: - ARSCNViewDelegate
  @objc_method
  def renderer_didAddNode_forAnchor_(self, renderer, node, anchor):
    if not isinstance((meshAnchor := anchor), ARMeshAnchor):
      return
    meshGeometry = ARSCNMeshGeometry(meshAnchor)
    meshNode = meshGeometry.setNode_(UIColor.systemCyanColor())
    meshNode.setName_(meshAnchor.identifier.UUIDString)

    node.addChildNode_(meshNode)

  @objc_method
  def renderer_didUpdateNode_forAnchor_(self, renderer, node, anchor):
    if not isinstance((meshAnchor := anchor), ARMeshAnchor):
      return

    if (previousMeshNode :=
        self.scnView.scene.rootNode.childNodeWithName_recursively_(
          identifier.UUIDString if
          (identifier := meshAnchor.identifier) else '', True)):
      previousMeshNode.removeFromParentNode()

    meshGeometry = ARSCNMeshGeometry(meshAnchor)
    meshNode = meshGeometry.setNode_(UIColor.systemCyanColor())
    meshNode.setName_(meshAnchor.identifier.UUIDString)

    node.addChildNode_(meshNode)

  # MARK: - ARSessionDelegate
  @objc_method
  def session_didUpdateFrame_(self, session, frame):
    #print('didUpdateFrame')
    pass

  @objc_method
  def session_didAddAnchors_(self, session, anchors):
    #print('didAddAnchors')
    pass

  @objc_method
  def session_didUpdateAnchors_(self, session, anchors):
    #print('didUpdateAnchors')
    pass

  @objc_method
  def session_didRemoveAnchors_(self, session, anchors):
    #print('didRemoveAnchors')
    pass


if __name__ == '__main__':
  from rbedge.app import App
  from objc_frameworks.UIKit import UIModalPresentationStyle

  main_vc = MainViewController.new()

  presentation_style = UIModalPresentationStyle.fullScreen
  #presentation_style = UIModalPresentationStyle.pageSheet

  app = App(main_vc, presentation_style)
  app.present()

